import os
import datetime
import sqlite3
import csv
from rich.console import Console
from app.db.session_db import get_connection

console = Console()

def export_session_to_csv():
    """Export each table in the session database into separate CSV files."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    export_dir = os.path.join("reports", f"session_{timestamp}")
    os.makedirs(export_dir, exist_ok=True)

    tables = [
        "targets",
        "domains",
        "emails",
        "ips",
        "hosts",
        "a_records",
        "ns_records",
        "mx_records",
        "txt_records",
        "srv_records",
        "soa_records",
        "enumerated_ips",
        "enumerated_domains",
        "user_whois_queries",
        "enumerated_nmap_ips",
        "enumerated_nmap_hosts",
        "user_nmap_queries"
    ]

    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            for table in tables:
                try:
                    cursor.execute(f"SELECT * FROM {table}")
                    rows = cursor.fetchall()
                    if not rows:
                        continue  # Skip empty tables

                    # Get column headers
                    column_names = [description[0] for description in cursor.description]

                    csv_path = os.path.join(export_dir, f"{table}.csv")
                    with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(column_names)  # Write headers
                        writer.writerows(rows)         # Write data

                    console.print(f"[green]Exported {table}.csv with {len(rows)} records.[/green]")

                except sqlite3.OperationalError:
                    # Table might not exist yet
                    continue

            console.print(f"\n[bold cyan]Export complete![/bold cyan] All CSV files saved to: [underline]{export_dir}[/underline]")

    except Exception as e:
        console.print(f"[red][!] Failed to export session: {e}[/red]")
