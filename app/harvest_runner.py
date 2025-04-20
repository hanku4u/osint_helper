# harvest_runner.py

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

def run_theharvester(session_manager):
    console.print(Panel("🔍 [bold cyan]Run theHarvester[/bold cyan]", expand=False))

    domain = Prompt.ask("Enter the domain to search")

    # Show the default values before asking
    print()
    console.print(Panel.fit(
        f"[bold]Default Arguments:[/bold]\n"
        f"- Sources: [green]{DEFAULT_SOURCES}[/green]\n"
        f"- Limit: [green]{DEFAULT_LIMIT}[/green]\n"
        f"- Start: [green]{DEFAULT_START}[/green]\n"
        f"- Verbose: [green]False[/green]",
        title="Default Settings",
        border_style="cyan"
    ))

    use_defaults = Prompt.ask(
        "Use default settings? [sources=all, limit=100, start=0, no verbose]",
        choices=["y", "n"],
        default="y"
    )

    if use_defaults.lower() == "y":
        sources = DEFAULT_SOURCES
        limit = DEFAULT_LIMIT
        start = DEFAULT_START
        verbose = False
    else:
        console.print("\n[bold]Available Sources:[/bold] [dim]baidu, bing, crtsh, duckduckgo, google, hunter, intelx, linkedin, netcraft, otx, qwant, rapiddns, securityTrails, sublist3r, threatcrowd, trello, twitter, virustotal, yahoo, etc.[/dim]")
        sources = Prompt.ask("Enter data sources (comma-separated)", default=DEFAULT_SOURCES)
        limit = IntPrompt.ask("Limit number of results", default=DEFAULT_LIMIT)
        start = IntPrompt.ask("Start from result number", default=DEFAULT_START)
        verbose = Prompt.ask("Verbose mode?", choices=["y", "n"], default="n").lower() == "y"

    # Prepare file paths
    output_dir = session_manager.get_output_path_for_tool("theHarvester")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    base_filename = f"theharvester_{domain}_{timestamp}"
    output_base_path = os.path.join(output_dir, base_filename)
    json_path = f"{output_base_path}.json"

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

    console.print(f"\n[bold green]Running:[/bold green] {' '.join(cmd)}\n")

    try:
        subprocess.run(cmd, check=True)
        console.print(f"[green]theHarvester output saved to:[/green] {json_path}")
    except subprocess.CalledProcessError:
        console.print(f"[bold red]Error:[/bold red] Failed to run theHarvester.")
        return

    # Parse results
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            data = json.load(f)

        emails = [e["email"] for e in data.get("emails", [])]
        hosts = [h["hostname"] for h in data.get("hosts", [])]
        ips = [h["ip"] for h in data.get("hosts", []) if "ip" in h]

        console.print(f"[cyan]Found:[/cyan] {len(emails)} emails, {len(hosts)} hosts, {len(ips)} IPs")

        console.print(f"[blue]Parsed Emails:[/blue] {emails}")
        console.print(f"[blue]Parsed Hosts:[/blue] {hosts}")
        console.print(f"[blue]Parsed IPs:[/blue] {ips}")
        print()

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
