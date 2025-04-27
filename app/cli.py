# app/cli.py

from rich.console import Console
from rich.prompt import Prompt
from app.tools.harvester_runner import run_theharvester

console = Console()

def main_menu():
    while True:
        console.print("\n[bold cyan]OSINT CLI Toolkit[/bold cyan]")
        console.print("[1] Run theHarvester")
        console.print("[2] Exit")

        choice = Prompt.ask("\nEnter your choice", choices=["1", "2"])

        if choice == "1":
            domain = Prompt.ask("Enter the domain or IP to scan")
            
            console.print("\n[bold green]Default Arguments:[/bold green]")
            console.print(f"-d {domain} -b all -l 100")

            console.print("\n[bold cyan]Available Additional Arguments:[/bold cyan]")
            console.print("""
            -S                    : Perform a DNS brute force
            -v                    : Enable verbose output
            -h                    : Show help message
            --sourcelist          : List available data sources
            --dns-server [server] : Use a specific DNS server
            --virtual-host        : Verify virtual hosts
            """)

            custom_args = Prompt.ask("\nEnter any additional arguments you want to use (or leave blank)", default="")

            custom_args = Prompt.ask("\nEnter any additional arguments you want to use (or leave blank)", default="")
            output_path = run_theharvester(domain, custom_args)

            if output_path:
                console.print(f"[green]Scan completed! Output saved to {output_path}[/green]")
            else:
                console.print("[red]Scan failed.[/red]")

        elif choice == "2":
            console.print("[yellow]Exiting...[/yellow]")
            break
