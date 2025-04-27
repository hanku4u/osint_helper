# app/tools/report_generator.py

import os
import datetime
import sqlite3
from rich.console import Console
from rich.prompt import Prompt
from app.db.session_db import get_connection

console = Console()

def header(text, level=1):
    """Generate a Markdown or Text header based on the output format."""
    if output_format == "markdown":
        return f"{'#' * level} {text}\n"
    else:
        return f"{text}\n{'=' * len(text)}\n"

def extract_nmap_summary(raw_text):
    """Extract ports/services summary from Nmap raw text."""
    lines = raw_text.splitlines()
    ports = []
    found_ports_section = False

    for line in lines:
        line = line.strip()

        if line.startswith("PORT"):
            found_ports_section = True
            continue

        if found_ports_section:
            if not line or line.startswith("Nmap done") or line.startswith("Service Info:"):
                break

            parts = line.split()
            if len(parts) >= 3:
                port_proto = parts[0]    # "22/tcp"
                service = parts[2]       # "ssh"
                version = " ".join(parts[3:]) if len(parts) > 3 else ""

                ports.append(f"- {port_proto} ({service}) {version}")

    return ports

def generate_session_report():
    """Generate a session report in markdown or text format."""
    global output_format
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

    try:
        with get_connection() as conn, open(report_path, "w", encoding="utf-8") as report:
            cursor = conn.cursor()

            # --- Header ---
            report.write(header("OSINT Session Report"))
            report.write(f"_Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n\n")

            # --- Session Summary ---
            report.write(header("Session Summary", level=2))

            for label, table in sections.items():
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    report.write(f"- {label}: {count}\n")
                except sqlite3.OperationalError:
                    continue

            report.write("\n")  # Blank line after summary

            # --- Detailed Sections ---
            for section_title, table_name in sections.items():
                try:
                    cursor.execute(f"SELECT * FROM {table_name}")
                    rows = cursor.fetchall()
                    if not rows:
                        continue

                    report.write(header(section_title, level=2))

                    # Special handling for Nmap tables
                    if table_name in ("enumerated_nmap_ips", "enumerated_nmap_hosts", "user_nmap_queries"):
                        for (id, raw_text) in rows:
                            ports = extract_nmap_summary(raw_text)
                            if ports:
                                report.write("\nHost:\n")
                                for port in ports:
                                    report.write(f"{port}\n")
                            else:
                                report.write("[No open ports found]\n")
                            report.write("\n")

                    else:
                        # Default handling for normal tables
                        for row in rows:
                            if len(row) == 2:
                                report.write(f"- {row[1]}\n")
                            else:
                                for item in row[1:]:
                                    if item:
                                        report.write(f"- {item}\n")
                                report.write("\n")

                except sqlite3.OperationalError:
                    continue

            console.print(f"[green]Report saved to: {report_path}[/green]")

    except Exception as e:
        console.print(f"[red][!] Failed to generate report: {e}[/red]")
