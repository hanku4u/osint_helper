from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from app.tools.harvester_runner import run_theharvester
from app.tools.dns_runner import run_dnsrecon
from app.db.session_db import fetch_targets, fetch_domains, fetch_emails, fetch_ips, fetch_hosts
import sqlite3
from app.db.session_db import get_connection

console = Console()

def run_sql_query(sql: str):
    """Run a SQL query against the current session DB and display results."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]

            if not rows:
                console.print("[yellow]No results found.[/yellow]")
                return

            # Paginate results
            page_size = 10
            total = len(rows)
            current = 0

            while current < total:
                table = Table(title=f"Query Results", show_lines=True)

                for column in columns:
                    table.add_column(column, style="cyan")

                end = min(current + page_size, total)
                for row in rows[current:end]:
                    table.add_row(*[str(item) if item is not None else "" for item in row])

                console.print(table)

                current = end
                if current >= total:
                    break

                user_input = Prompt.ask("View next page? (n to continue, q to quit)", choices=["n", "q"], default="n")
                if user_input == "q":
                    break

    except sqlite3.OperationalError as e:
        console.print(f"[red][!] SQL error: {e}[/red]")
    except Exception as e:
        console.print(f"[red][!] Unexpected error running query: {e}[/red]")


def main_menu():
    while True:
        console.print("\n[bold cyan]OSINT CLI Toolkit[/bold cyan]")
        console.print("[1] Run theHarvester")
        console.print("[2] Run DNS Enumeration")
        console.print("[3] Review Current Session Data")
        console.print("[4] Exit")

        choice = Prompt.ask("\nEnter your choice", choices=["1", "2", "3", "4"])

        if choice == "1":
            domain = Prompt.ask("Enter the domain or IP to scan with theHarvester")
            
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
            domain = Prompt.ask("Enter the domain to scan with dnsrecon")
            
            console.print("\n[bold green]Default Arguments:[/bold green]")
            console.print(f"-d {domain}")

            console.print("\n[bold cyan]Available Additional Arguments:[/bold cyan]")
            console.print("""
-t standard          : Perform a standard DNS enumeration
-t axfr              : Attempt DNS zone transfer
-t brt               : Perform a DNS brute-force
--xml <filename>     : Output results to an XML file
-h                   : Show help message
""")

            custom_args = Prompt.ask("\nEnter any additional arguments you want to use (or leave blank)", default="")
            output_path = run_dnsrecon(domain, custom_args)
            
            if output_path:
                console.print(f"[green]Scan completed! Output saved to {output_path}[/green]")
            else:
                console.print("[red]Scan failed.[/red]")

        elif choice == "3":
            while True:
                console.print("\n[bold cyan]Review Session Data[/bold cyan]")
                console.print("[1] View targets table")
                console.print("[2] View domains table")
                console.print("[3] View emails table")
                console.print("[4] View IPs table")
                console.print("[5] View hosts table")
                console.print("[6] View TXT records table")
                console.print("[7] View SRV records table")
                console.print("[8] Run a custom SQL query")
                console.print("[9] Return to Main Menu")

                review_choice = Prompt.ask("\nSelect an option", choices=[str(i) for i in range(1, 10)])

                if review_choice == "1":
                    run_sql_query("SELECT * FROM targets;")
                elif review_choice == "2":
                    run_sql_query("SELECT * FROM domains;")
                elif review_choice == "3":
                    run_sql_query("SELECT * FROM emails;")
                elif review_choice == "4":
                    run_sql_query("SELECT * FROM ips;")
                elif review_choice == "5":
                    run_sql_query("SELECT * FROM hosts;")
                elif review_choice == "6":
                    run_sql_query("SELECT * FROM txt_records;")
                elif review_choice == "7":
                    run_sql_query("SELECT * FROM srv_records;")
                elif review_choice == "8":
                    custom_sql = Prompt.ask("Enter your custom SQL query (e.g., SELECT * FROM hosts WHERE host LIKE '%admin%')")
                    run_sql_query(custom_sql)
                elif review_choice == "9":
                    break


        elif choice == "4":
            console.print("[yellow]Exiting...[/yellow]")
            break
