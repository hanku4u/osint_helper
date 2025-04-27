# app/tools/nmap_runner.py

import subprocess
import datetime
import os
from rich.console import Console
from rich.prompt import Prompt
from app.db.session_db import (
    get_all_ips,
    get_all_hosts,
    insert_enumerated_nmap_ip,
    insert_enumerated_nmap_host,
    insert_user_nmap_query
)

console = Console()

RESULTS_DIR = "results"

def run_nmap_menu():
    """Present Nmap options to the user."""
    while True:
        console.print("\n[bold cyan]Nmap Enumeration Menu[/bold cyan]")
        console.print("[1] Scan IPs found in session")
        console.print("[2] Scan Hosts found in session")
        console.print("[3] Custom Nmap scan")
        console.print("[4] Return to Main Menu")

        choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4"])

        if choice == "1":
            ips = get_all_ips()
            if not ips:
                console.print("[yellow]No IP addresses found in session.[/yellow]")
                continue

            for (ip,) in ips:
                run_and_store_nmap(ip, record_type="ip")

        elif choice == "2":
            hosts = get_all_hosts()
            if not hosts:
                console.print("[yellow]No hosts found in session.[/yellow]")
                continue

            for (host,) in hosts:
                run_and_store_nmap(host, record_type="host")

        elif choice == "3":
            custom_target = Prompt.ask("Enter an IP address or hostname to scan")
            run_and_store_nmap(custom_target, record_type="custom")

        elif choice == "4":
            break

def run_and_store_nmap(target: str, record_type: str):
    """Run Nmap scan and store the result."""
    os.makedirs(RESULTS_DIR, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"nmap_{target}_{timestamp}.txt"
    output_path = os.path.join(RESULTS_DIR, output_filename)

    # Default arguments: service/version detection, top 10 ports
    command = ["nmap", "-sV", "--top-ports", "10", target]
    full_command_str = " ".join(command)

    try:
        with console.status(f"[bold green]Running: {full_command_str}[/bold green]", spinner="dots"):
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

        with open(output_path, "w") as f:
            f.write(result.stdout)

        if result.returncode != 0:
            console.print(f"[red][!] nmap returned an error (exit code {result.returncode}):[/red]")
            console.print(result.stdout)
            return

        parse_and_store_nmap_output(target, output_path, record_type)

    except Exception as e:
        console.print(f"[red][!] Unexpected error running nmap: {e}[/red]")

def parse_and_store_nmap_output(target: str, filepath: str, record_type: str):
    """Parse Nmap output and insert structured data into the session DB."""
    try:
        ports_info = []
        raw_text = ""

        with open(filepath, "r") as f:
            lines = f.readlines()
            raw_text = "".join(lines)

        parsing_ports = False

        for line in lines:
            line = line.strip()

            if line.startswith("PORT"):
                parsing_ports = True
                continue

            if parsing_ports:
                if line == "" or "Nmap done" in line:
                    break

                parts = line.split()
                if len(parts) >= 3:
                    port_protocol = parts[0]  # like "22/tcp"
                    service = parts[2]
                    version = " ".join(parts[3:]) if len(parts) > 3 else ""

                    port, protocol = port_protocol.split("/")

                    ports_info.append((port, protocol, service, version))

        for (port, protocol, service, version) in ports_info:
            if record_type == "ip":
                insert_enumerated_nmap_ip(target, port, protocol, service, version, raw_text)
            elif record_type == "host":
                insert_enumerated_nmap_host(target, port, protocol, service, version, raw_text)
            elif record_type == "custom":
                insert_user_nmap_query(target, port, protocol, service, version, raw_text)

    except Exception as e:
        console.print(f"[red][!] Failed to parse Nmap output: {e}[/red]")
