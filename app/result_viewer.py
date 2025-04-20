# result_viewer.py

import os
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
import questionary

console = Console()

def review_results(session_manager):
    pool = session_manager.get_result_pool()

    if not any(pool.values()):
        console.print("[yellow]No results available yet to review.[/yellow]")
        return

    while True:
        filter_keyword = Prompt.ask("\nEnter a search keyword to filter results (or leave blank to show all)", default="").lower()
        filtered_pool = {
            k: [item for item in v if filter_keyword in item.lower()] if filter_keyword else v
            for k, v in pool.items()
        }

        table = Table(title="🔍 theHarvester Results", expand=True)
        table.add_column("Type", style="bold cyan")
        table.add_column("Value", style="white")

        count = 0
        for key, values in filtered_pool.items():
            for value in values:
                table.add_row(key, value)
                count += 1

        if count == 0:
            console.print("[italic]No matching results found.[/italic]")
        else:
            console.print(table)

        again = Prompt.ask("Search again?", choices=["y", "n"], default="n")
        if again.lower() != "y":
            break

def select_from_result_pool(session_manager, type_filter: str) -> list[str]:
    pool = session_manager.get_result_pool()
    values = pool.get(type_filter, [])

    if not values:
        console.print(f"[yellow]No values found for type: {type_filter}[/yellow]")
        return []

    selected = questionary.checkbox(
        f"Select {type_filter} values to use:",
        choices=values
    ).ask()

    if not selected:
        console.print("[italic]No selections made.[/italic]")

    return selected or []

def view_nmap_services(session_manager):
    services = session_manager.get_result_pool().get("nmap_services", [])

    if not services:
        console.print("[yellow]No Nmap services found in this session.[/yellow]")
        return

    keyword = Prompt.ask("Enter keyword to filter (press Enter to skip)", default="").lower()

    filtered = []
    for entry in services:
        match = (
            keyword in entry["port"].lower()
            or keyword in entry["service"].lower()
            or keyword in entry["version"].lower()
            or keyword in entry["target"].lower()
        ) if keyword else True

        if match:
            filtered.append(entry)

    if not filtered:
        console.print("[italic]No matching results found.[/italic]")
        return

    table = Table(title="📡 Nmap Discovered Services", expand=True)
    table.add_column("Target", style="cyan")
    table.add_column("Port", style="magenta")
    table.add_column("Service", style="green")
    table.add_column("Version", style="white")

    for entry in filtered:
        table.add_row(
            entry["target"],
            entry["port"],
            entry["service"],
            entry["version"]
        )

    console.print(table)

def view_dns_results(session_manager):
    base_dir = session_manager.session_path
    dns_dirs = {
        "dnsrecon": os.path.join(base_dir, "dnsrecon"),
        "amass": os.path.join(base_dir, "amass"),
        "fierce": os.path.join(base_dir, "fierce")
    }

    all_files = []
    for tool, path in dns_dirs.items():
        if os.path.exists(path):
            for file in os.listdir(path):
                if file.endswith(".txt"):
                    full_path = os.path.join(path, file)
                    all_files.append((f"{tool} → {file}", full_path))

    if not all_files:
        console.print("[yellow]No DNS result files found in this session.[/yellow]")
        return

    choices = [label for label, _ in all_files]
    selected = questionary.checkbox("Select DNS result files to view:", choices=choices).ask()

    if not selected:
        console.print("[italic]No files selected.[/italic]")
        return

    for label in selected:
        filepath = next(path for l, path in all_files if l == label)
        console.rule(label)
        try:
            with open(filepath, "r") as f:
                content = f.read()
            console.print(Panel.fit(content, title=os.path.basename(filepath), padding=(1, 2)))
        except Exception as e:
            console.print(f"[red]Failed to read {filepath}: {e}[/red]")

def view_searchsploit_results(session_manager):
    base_dir = session_manager.get_output_path_for_tool("searchsploit")

    if not os.path.exists(base_dir):
        console.print("[yellow]No Searchsploit results directory found.[/yellow]")
        return

    files = [
        os.path.join(base_dir, f) for f in os.listdir(base_dir)
        if f.endswith(".txt")
    ]

    if not files:
        console.print("[yellow]No Searchsploit results found in this session.[/yellow]")
        return

    labels = [os.path.basename(f) for f in files]
    selected = questionary.checkbox("Select Searchsploit results to view:", choices=labels).ask()

    if not selected:
        console.print("[italic]No files selected.[/italic]")
        return

    for label in selected:
        filepath = os.path.join(base_dir, label)
        console.rule(label)
        try:
            with open(filepath, "r") as f:
                content = f.read()
            console.print(Panel.fit(content, title=label, padding=(1, 2)))
        except Exception as e:
            console.print(f"[red]Error reading file {label}[/red]: {e}")

import json
from rich.panel import Panel

def view_shodan_results(session_manager):
    base_dir = session_manager.get_output_path_for_tool("shodan")

    if not os.path.exists(base_dir):
        console.print("[yellow]No Shodan results directory found.[/yellow]")
        return

    files = [
        os.path.join(base_dir, f) for f in os.listdir(base_dir)
        if f.endswith(".json")
    ]

    if not files:
        console.print("[yellow]No Shodan result files found in this session.[/yellow]")
        return

    labels = [os.path.basename(f) for f in files]
    selected = questionary.checkbox("Select Shodan results to view:", choices=labels).ask()

    if not selected:
        console.print("[italic]No files selected.[/italic]")
        return

    for label in selected:
        filepath = os.path.join(base_dir, label)
        console.rule(label)
        try:
            with open(filepath, "r") as f:
                data = json.load(f)

            ip = data.get("ip_str", "N/A")
            org = data.get("org", "N/A")
            isp = data.get("isp", "N/A")
            hostnames = ", ".join(data.get("hostnames", []))
            ports = ", ".join(str(p) for p in data.get("ports", []))
            location = f"{data.get('city', '')}, {data.get('country_name', '')}".strip(", ")

            content = f"""
[bold]IP:[/bold] {ip}
[bold]Org:[/bold] {org}
[bold]ISP:[/bold] {isp}
[bold]Hostnames:[/bold] {hostnames}
[bold]Ports:[/bold] {ports}
[bold]Location:[/bold] {location}
"""

            console.print(Panel.fit(content, title=ip, padding=(1, 2)))

        except Exception as e:
            console.print(f"[red]Error reading or parsing {label}: {e}[/red]")
