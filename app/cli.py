# app/cli.py

from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
import sqlite3
import os

from app.tools.harvester_runner import run_theharvester
from app.tools.dns_runner import run_dnsrecon
from app.tools.whois_runner import run_whois_menu
from app.tools.nmap_runner import run_nmap_menu
from app.db.session_db import get_connection

console = Console()

# Tables to display and their friendly labels
TABLES_TO_DISPLAY = [
    ("targets", "Targets"),
    ("domains", "Domains"),
    ("emails", "Emails"),
    ("ips", "IP Addresses"),
    ("hosts", "Hosts"),
    ("a_records", "A Records"),
    ("ns_records", "NS Records"),
    ("mx_records", "MX Records"),
    ("txt_records", "TXT Records"),
    ("srv_records", "SRV Records"),
    ("soa_records", "SOA Records"),
    ("enumerated_ips", "WHOIS - Enumerated IPs"),
    ("enumerated_domains", "WHOIS - Enumerated Domains"),
    ("user_whois_queries", "WHOIS - Custom Queries"),
    ("enumerated_nmap_ips", "Nmap - Scanned IPs"),
    ("enumerated_nmap_hosts", "Nmap - Scanned Hosts"),
    ("user_nmap_queries", "Nmap - Custom Queries"),
]

def get_table_count(table_name):
    """Return the number of records in a table."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            result = cursor.fetchone()
            return result[0] if result else 0
    except sqlite3.OperationalError:
        return 0  # Table doesn't exist yet

def run_sql_query(sql: str):
    """Run a SQL query against the current session DB and display results paginated."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]

            if not rows:
                console.print("[yellow]No results found.[/yellow]")
                return

            page_size = 10
            total = len(rows)
            current = 0

            while current < total:
                table = Table(title="Query Results", show_lines=True)
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

def review_session_data_menu():
    """Show the dynamic session data review menu with record counts."""
    while True:
        console.print("\n[bold cyan]Review Session Data[/bold cyan]")

        for idx, (table_name, label) in enumerate(TABLES_TO_DISPLAY, start=1):
            count = get_table_count(table_name)
            console.print(f"[{idx}] {label} ({count} records)")

        console.print(f"[{len(TABLES_TO_DISPLAY)+1}] Run a custom SQL query")
        console.print(f"[{len(TABLES_TO_DISPLAY)+2}] Return to Main Menu")

        choices = [str(i) for i in range(1, len(TABLES_TO_DISPLAY) + 3)]
        review_choice = Prompt.ask("\nSelect an option", choices=choices)

        review_choice = int(review_choice)

        if 1 <= review_choice <= len(TABLES_TO_DISPLAY):
            table_name, label = TABLES_TO_DISPLAY[review_choice - 1]
            run_sql_query(f"SELECT * FROM {table_name};")

        elif review_choice == len(TABLES_TO_DISPLAY) + 1:
            custom_sql = Prompt.ask("Enter your custom SQL query (e.g., SELECT * FROM hosts WHERE host LIKE '%admin%')")
            run_sql_query(custom_sql)

        elif review_choice == len(TABLES_TO_DISPLAY) + 2:
            break

def main_menu():
    """Main OSINT CLI Toolkit menu."""
    while True:
        console.print("\n[bold cyan]OSINT CLI Toolkit[/bold cyan]")
        console.print("[1] Run theHarvester")
        console.print("[2] Run DNS Enumeration (dnsrecon)")
        console.print("[3] Run WHOIS Enumeration")
        console.print("[4] Run Nmap Scan")      # 👈 ADD THIS
        console.print("[5] Review Current Session Data")
        console.print("[6] Exit")

        choice = Prompt.ask("\nEnter your choice", choices=["1", "2", "3", "4", "5", "6"])

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
            console.print(f"-d {domain} -j [output.json]")

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
            run_whois_menu()

        elif choice == "4":
            run_nmap_menu()
        
        elif choice == "5":
            review_session_data_menu()

        elif choice == "6":
            console.print("[yellow]Exiting...[/yellow]")
            break
