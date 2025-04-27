# app/tools/whois_runner.py

import subprocess
import datetime
import os
from rich.console import Console
from rich.prompt import Prompt
from app.db.session_db import (
    insert_enumerated_ip,
    insert_enumerated_domain,
    insert_user_whois_query,
    get_all_ips,
    get_all_domains
)

console = Console()

RESULTS_DIR = "results"

def run_whois_menu():
    """Present WHOIS options to the user."""
    while True:
        console.print("\n[bold cyan]WHOIS Enumeration Menu[/bold cyan]")
        console.print("[1] Enumerate IPs found in session")
        console.print("[2] Enumerate Domains found in session")
        console.print("[3] Custom WHOIS lookup")
        console.print("[4] Return to Main Menu")

        choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4"])

        if choice == "1":
            ips = get_all_ips()
            if not ips:
                console.print("[yellow]No IP addresses found in session.[/yellow]")
                continue

            for (ip,) in ips:
                run_and_store_whois(ip, record_type="ip")

        elif choice == "2":
            domains = get_all_domains()
            if not domains:
                console.print("[yellow]No domains found in session.[/yellow]")
                continue

            for (domain,) in domains:
                run_and_store_whois(domain, record_type="domain")

        elif choice == "3":
            custom_query = Prompt.ask("Enter an IP address or domain name to query")
            run_and_store_whois(custom_query, record_type="custom")

        elif choice == "4":
            break

def run_and_store_whois(target: str, record_type: str):
    """Run WHOIS lookup and store the result in the correct table."""
    os.makedirs(RESULTS_DIR, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"whois_{target}_{timestamp}.txt"
    output_path = os.path.join(RESULTS_DIR, output_filename)

    command = ["whois", target]

    try:
        with console.status(f"[bold green]Running: whois {target}[/bold green]", spinner="dots"):
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

        with open(output_path, "w") as f:
            f.write(result.stdout)

        if result.returncode != 0:
            console.print(f"[red][!] whois returned an error (exit code {result.returncode}):[/red]")
            console.print(result.stdout)
            return

        # ✅ Parse the WHOIS output and insert it
        parse_and_store_whois_output(target, output_path, record_type)

    except Exception as e:
        console.print(f"[red][!] Unexpected error running whois: {e}[/red]")

def parse_and_store_whois_output(target: str, filepath: str, record_type: str):
    """Parse WHOIS text and insert into appropriate session DB table."""
    try:
        registrar = None
        creation_date = None
        expiration_date = None
        name_servers = []

        with open(filepath, "r") as f:
            lines = f.readlines()

        raw_text = "".join(lines)

        for line in lines:
            line = line.strip()

            if line.lower().startswith("registrar:"):
                registrar = line.split(":", 1)[1].strip()

            elif "creation date" in line.lower():
                creation_date = line.split(":", 1)[1].strip()

            elif "expiration date" in line.lower():
                expiration_date = line.split(":", 1)[1].strip()

            elif line.lower().startswith("name server:"):
                ns = line.split(":", 1)[1].strip()
                name_servers.append(ns)

        if record_type == "ip":
            insert_enumerated_ip(target, registrar, creation_date, expiration_date, ", ".join(name_servers), raw_text)

        elif record_type == "domain":
            insert_enumerated_domain(target, registrar, creation_date, expiration_date, ", ".join(name_servers), raw_text)

        elif record_type == "custom":
            insert_user_whois_query(target, registrar, creation_date, expiration_date, ", ".join(name_servers), raw_text)

    except Exception as e:
        console.print(f"[red][!] Failed to parse WHOIS output: {e}[/red]")
