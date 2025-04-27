import os
import datetime
import sqlite3
from rich.console import Console
from rich.prompt import Prompt
from app.db.session_db import get_connection

console = Console()

def generate_session_report():
    """Generate a session report in markdown or text format."""
    output_format = Prompt.ask("\nSelect output format", choices=["markdown", "text"])

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = "reports"
    os.makedirs(report_dir, exist_ok=True)

    extension = "md" if output_format == "markdown" else "txt"
    report_path = os.path.join(report_dir, f"session_report_{timestamp}.{extension}")

    sections = {
        "Targets": "targets",
        "Domains": "domains",
        "Emails": "emails",
        "IP Addresses": "ips",
        "Hosts": "hosts",
        "A Records": "a_records",
        "NS Records": "ns_records",
        "MX Records": "mx_records",
        "TXT Records": "txt_records",
        "SRV Records": "srv_records",
        "SOA Records": "soa_records",
        "WHOIS - Enumerated IPs": "enumerated_ips",
        "WHOIS - Enumerated Domains": "enumerated_domains",
        "WHOIS - Custom Queries": "user_whois_queries",
        "Nmap - Scanned IPs": "enumerated_nmap_ips",
        "Nmap - Scanned Hosts": "enumerated_nmap_hosts",
        "Nmap - Custom Queries": "user_nmap_queries",
    }

    def header(text, level=1):
        if output_format == "markdown":
            return f"{'#' * level} {text}\n"
        else:
            return f"{text}\n{'=' * len(text)}\n"

    try:
        with get_connection() as conn, open(report_path, "w", encoding="utf-8") as report:
            # Header
            report.write(header("OSINT Session Report"))
            report.write(f"_Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n\n")

            cursor = conn.cursor()

            for section_title, table_name in sections.items():
                try:
                    cursor.execute(f"SELECT * FROM {table_name}")
                    rows = cursor.fetchall()
                    if not rows:
                        continue

                    report.write(header(section_title, level=2))

                    for row in rows:
                        # If single column table
                        if len(row) == 2:
                            report.write(f"- {row[1]}\n")
                        else:
                            for item in row[1:]:
                                if item:
                                    report.write(f"- {item}\n")
                            report.write("\n")

                except sqlite3.OperationalError:
                    # If the table does not exist, just skip it
                    continue

            console.print(f"[green]Report saved to: {report_path}[/green]")

    except Exception as e:
        console.print(f"[red][!] Failed to generate report: {e}[/red]")
