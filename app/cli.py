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

            # Remove duplicate arguments if user provides them
            forbidden_args = ["-d", "-b", "-l"]

            # Split their input into parts
            user_args_list = custom_args.split()

            # Filter out forbidden arguments
            filtered_args = []
            skip_next = False
            for i, arg in enumerate(user_args_list):
                if skip_next:
                    skip_next = False
                    continue

                if arg in forbidden_args:
                    console.print(f"[yellow]Skipping redundant argument: {arg}[/yellow]")
                    # If the argument expects a value, skip the next item too
                    if i + 1 < len(user_args_list) and not user_args_list[i+1].startswith('-'):
                        skip_next = True
                else:
                    filtered_args.append(arg)

            clean_custom_args = " ".join(filtered_args)

            output_path = run_theharvester(domain, clean_custom_args)

            if output_path:
                console.print(f"[green]Scan completed! Output saved to {output_path}[/green]")
            else:
                console.print("[red]Scan failed.[/red]")

        elif choice == "2":
            console.print("[yellow]Exiting...[/yellow]")
            break
