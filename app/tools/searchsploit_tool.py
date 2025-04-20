# tools/searchsploit_tool.py

import subprocess
import os
from datetime import datetime
from rich.console import Console
from rich.prompt import Prompt
from result_viewer import select_from_result_pool
import questionary

console = Console()

def run_searchsploit(session_manager):
    def get_search_terms():
        if use_services == "Select Nmap services":
            services = session_manager.get_result_pool().get("nmap_services", [])
            if not services:
                console.print("[yellow]No Nmap services available to search.[/yellow]")
                return []

            labels = [
                f"{s['target']} → {s['port']} {s['service']} {s['version']}"
                for s in services
            ]
            selected = questionary.checkbox("Select services to search:", choices=labels).ask()
            return [
                f"{s['service']} {s['version']}".strip()
                for label in selected
                for s in services
                if label == f"{s['target']} → {s['port']} {s['service']} {s['version']}"
            ]

        elif use_services == "Enter a manual search term":
            return [Prompt.ask("Enter your search query")]

    use_services = questionary.select(
        "Search exploits by:",
        choices=["Select Nmap services", "Enter a manual search term", "Cancel"]
    ).ask()

    if use_services == "Cancel":
        return

    search_terms = get_search_terms()
    if not search_terms:
        return

    # Run searchsploit for each search term
    output_dir = session_manager.get_output_path_for_tool("searchsploit")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    for term in search_terms:
        safe_term = term.replace(" ", "_").replace("/", "_")
        base_filename = f"searchsploit_{safe_term}_{timestamp}.txt"
        output_path = os.path.join(output_dir, base_filename)

        cmd = ["searchsploit", term]
        console.print(f"[bold green]Running:[/bold green] {' '.join(cmd)}")

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            with open(output_path, "w") as f:
                f.write(result.stdout)

            console.print(f"[green]Search results saved to:[/green] {output_path}")

            session_manager.add_tool_run(
                tool_name="searchsploit",
                input_value=term,
                output_file=os.path.basename(output_path),
                parsed_file=None
            )

        except subprocess.CalledProcessError as e:
            console.print(f"[red]Searchsploit failed for query: {term}[/red]")
            with open(output_path, "w") as f:
                f.write(e.stdout or "")
                f.write(e.stderr or "")
