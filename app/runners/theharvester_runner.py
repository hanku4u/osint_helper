import subprocess
import os
import json
from datetime import datetime
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.panel import Panel

console = Console()

DEFAULT_SOURCES = "all"
DEFAULT_LIMIT = 100
DEFAULT_START = 0

def run_theharvester(domain, session_manager):
    output_dir = session_manager.get_output_path_for_tool("theHarvester")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    base_filename = f"theharvester_{domain}_{timestamp}"
    output_base_path = os.path.join(output_dir, base_filename)
    json_path = f"{output_base_path}.json"

    console.print(Panel("🛠️ [bold cyan]Configure theHarvester[/bold cyan]", expand=False))

    use_defaults = Prompt.ask("Use default settings? [domain, sources=all, limit=100, start=0, no verbose]", choices=["y", "n"], default="y")

    if use_defaults == "y":
        sources = DEFAULT_SOURCES
        limit = DEFAULT_LIMIT
        start = DEFAULT_START
        verbose = False
    else:
        console.print("\n[bold]Available Sources:[/bold] [dim]baidu, bing, bingapi, crtsh, dnsdumpster, duckduckgo, google, googleCSE, hunter, intelx, linkedin, linkedin_links, netcraft, otx, qwant, rapiddns, securityTrails, sitedossier, spyse, sublist3r, threatcrowd, trello, twitter, virustotal, yahoo[/dim]")
        sources = Prompt.ask("Enter data sources (comma-separated)", default=DEFAULT_SOURCES)

        limit = IntPrompt.ask("Result limit", default=DEFAULT_LIMIT)
        start = IntPrompt.ask("Result start index", default=DEFAULT_START)

        verbose = Prompt.ask("Verbose mode?", choices=["y", "n"], default="n") == "y"

    # Build command
    cmd = [
        "theHarvester",
        "-d", domain,
        "-b", sources,
        "-l", str(limit),
        "-S", str(start),
        "-f", output_base_path
    ]

    if verbose:
        cmd.append("-v")

    console.print(f"\n[bold green]Executing:[/bold green] {' '.join(cmd)}\n")

    try:
        subprocess.run(cmd, check=True)
        console.print(f"[green]Output saved to:[/green] {json_path}")

        # Parse theHarvester JSON output
        if os.path.exists(json_path):
            with open(json_path, "r") as f:
                data = json.load(f)

            emails = [entry["email"] for entry in data.get("emails", [])]
            hosts = [entry["hostname"] for entry in data.get("hosts", [])]
            ips = [entry["ip"] for entry in data.get("hosts", []) if "ip" in entry]

            console.print(f"[cyan]Found {len(emails)} emails, {len(hosts)} hosts, {len(ips)} IPs.[/cyan]")

            session_manager.update_result_pool("emails", emails)
            session_manager.update_result_pool("subdomains", hosts)
            session_manager.update_result_pool("ips", ips)

            session_manager.add_tool_run(
                tool_name="theHarvester",
                input_value=domain,
                output_file=os.path.basename(json_path),
                parsed_file=os.path.basename(json_path)
            )
        else:
            console.print(f"[yellow]Warning: JSON output file not found at {json_path}[/yellow]")

    except subprocess.CalledProcessError:
        console.print(f"[bold red]Error:[/bold red] Failed to run theHarvester on {domain}")
