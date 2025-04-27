from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from app.tools.harvester_runner import run_theharvester
from app.db.session_db import fetch_targets, fetch_domains, fetch_emails, fetch_ips, fetch_hosts

console = Console()

def main_menu():
    while True:
        console.print("\n[bold cyan]OSINT CLI Toolkit[/bold cyan]")
        console.print("[1] Run theHarvester")
        console.print("[2] Review Current Session Data")
        console.print("[3] Exit")

        choice = Prompt.ask("\nEnter your choice", choices=["1", "2", "3"])

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
--dns-server          : Use a specific DNS server
--virtual-host        : Verify virtual hosts
""")

            custom_args = Prompt.ask("\nEnter any additional arguments you want to use (or leave blank)", default="")
            output_path = run_theharvester(domain, custom_args)
            
            if output_path:
                console.print(f"[green]Scan completed! Output saved to {output_path}[/green]")
            else:
                console.print("[red]Scan failed.[/red]")

        elif choice == "2":
            console.print("\n[bold cyan]Current Session Data:[/bold cyan]")

            # Targets
            targets = fetch_targets()
            if targets:
                console.print("\n[bold green]Targets:[/bold green]")
                for target in targets:
                    console.print(f"- {target[0]}")

            # Emails
            emails = fetch_emails()
            if emails:
                from rich.table import Table
                table = Table(title="Emails", show_lines=True)
                table.add_column("Email", style="cyan")
                for email in emails:
                    table.add_row(email[0])
                console.print(table)

            # IPs
            ips = fetch_ips()
            if ips:
                table = Table(title="IP Addresses", show_lines=True)
                table.add_column("IP Address", style="yellow")
                for ip in ips:
                    table.add_row(ip[0])
                console.print(table)

            # Hosts
            hosts = fetch_hosts()
            if hosts:
                table = Table(title="Hosts", show_lines=True)
                table.add_column("Host", style="green")
                for host in hosts:
                    table.add_row(host[0])
                console.print(table)

            # Domains (optional if you add domain parsing later)
            domains = fetch_domains()
            if domains:
                table = Table(title="Domains", show_lines=True)
                table.add_column("Domain", style="magenta")
                for domain in domains:
                    table.add_row(domain[0])
                console.print(table)

        elif choice == "3":
            console.print("[yellow]Exiting...[/yellow]")
            break
