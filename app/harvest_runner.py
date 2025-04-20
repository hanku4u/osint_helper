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

# List of valid sources for theHarvester
VALID_SOURCES = [
    "anubis", "baidu", "bevigil", "binaryedge", "bing", "bingapi", "bufferoverun", "brave",
    "censys", "certspotter", "criminalip", "crtsh", "dnsdumpster", "duckduckgo", "fullhunt",
    "github-code", "hackertarget", "hunter", "hunterhow", "intelx", "netlas", "onyphe", "otx",
    "pentesttools", "projectdiscovery", "rapiddns", "rocketreach", "securityTrails", "sitedossier",
    "subdomaincenter", "subdomainfinderc99", "threatminer", "tomba", "urlscan", "virustotal",
    "yahoo", "zoomeye" 
]

def run_theharvester(session_manager):
    console.print(Panel("🔍 [bold cyan]Run theHarvester[/bold cyan]", expand=False))

    domain = Prompt.ask("Enter the domain or IP to search")

    # Show the default values before asking
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
        console.print("\n[bold]Available Sources:[/bold] [dim]" + ", ".join(VALID_SOURCES) + "[/dim]")
        
        while True:
            sources = Prompt.ask("Enter data sources (comma-separated)", default=DEFAULT_SOURCES)
            selected_sources = [s.strip() for s in sources.split(",")]
            
            # Validate sources
            invalid_sources = [s for s in selected_sources if s not in VALID_SOURCES]
            if invalid_sources:
                console.print(f"[bold red]Invalid sources:[/bold red] {', '.join(invalid_sources)}")
                console.print("[yellow]Please enter valid sources from the list above.[/yellow]")
            else:
                break

        limit = IntPrompt.ask("Limit number of results", default=DEFAULT_LIMIT)
        start = IntPrompt.ask("Start from result number", default=DEFAULT_START)
        verbose = Prompt.ask("Verbose mode?", choices=["y", "n"], default="n").lower() == "y"

    # Prepare output path
    output_dir = session_manager.get_output_path_for_tool("theHarvester")
    os.makedirs(output_dir, exist_ok=True)  # Ensure directory exists

    safe_name = domain.replace(".", "_")  # Safe for filename
    json_path = os.path.join(output_dir, f"theharvester_{safe_name}.json")

    # Build theHarvester command
    cmd = [
        "theHarvester",
        "-d", domain,
        "-b", sources,
        "-l", str(limit),
        "-S", str(start),
        "-f", json_path  # Specify the full path including .json
    ]
    if verbose:
        cmd.append("-v")

    console.print(f"\n[bold green]Running:[/bold green] {' '.join(cmd)}\n")

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        console.print(f"[bold red]Error:[/bold red] Failed to run theHarvester.")
        return

    # Check if output file was created
    if os.path.exists(json_path):
        console.print(f"[green]theHarvester output saved to:[/green] {json_path}")

        with open(json_path, "r") as f:
            data = json.load(f)

        # Safely extract emails
        emails = [e["email"] for e in data.get("emails", []) if isinstance(e, dict) and "email" in e]

        host_entries = data.get("hosts", [])
        if host_entries and isinstance(host_entries[0], str):
            hosts = host_entries
            ips = []
        else:
            hosts = [h["hostname"] for h in host_entries if isinstance(h, dict) and "hostname" in h]
            ips = [h["ip"] for h in host_entries if isinstance(h, dict) and "ip" in h]

        console.print(f"[cyan]Found:[/cyan] {len(emails)} emails, {len(hosts)} hosts, {len(ips)} IPs")

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
