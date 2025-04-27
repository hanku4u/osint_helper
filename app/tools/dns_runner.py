# app/tools/dns_runner.py

import subprocess
import datetime
import os
from rich.console import Console
from app.db.session_db import insert_domain, insert_ip

console = Console()

RESULTS_DIR = "results"

def run_dnsrecon(domain: str, custom_args: str = "") -> str:
    """Run dnsrecon on a domain, parse output, and store results."""
    os.makedirs(RESULTS_DIR, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"dnsrecon_{domain}_{timestamp}.txt"
    output_path = os.path.join(RESULTS_DIR, output_filename)

    # Build command
    base_args = [
        "-d", domain
    ]

    user_args = custom_args.split() if custom_args else []

    command = ["dnsrecon"] + base_args + user_args

    try:
        full_command_str = " ".join(command)

        with console.status(f"[bold green]Running: {full_command_str}[/bold green]", spinner="dots"):
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

        with open(output_path, "w") as output_file:
            output_file.write(result.stdout)

        if result.returncode != 0:
            console.print(f"[red][!] dnsrecon returned an error (exit code {result.returncode}):[/red]")
            console.print(result.stdout)
            return ""

        # ✅ After successful scan, parse output
        parse_and_store_dnsrecon_output(output_path)

    except Exception as e:
        console.print(f"[red][!] Unexpected error running dnsrecon: {e}[/red]")
        return ""

    return output_path

def parse_and_store_dnsrecon_output(filepath):
    """Parse dnsrecon text output and insert found domains into the session database."""
    try:
        with open(filepath, "r") as file:
            lines = file.readlines()

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # dnsrecon output usually contains discovered hosts like this:
            # [+] Hostname found: www.example.com IP: 1.2.3.4

            if "Hostname found:" in line:
                parts = line.split()
                if "Hostname" in parts and "IP:" in parts:
                    hostname_index = parts.index("Hostname") + 2  # Hostname is after "Hostname found:"
                    ip_index = parts.index("IP:") + 1

                    domain = parts[hostname_index].strip()
                    ip = parts[ip_index].strip()

                    if domain:
                        insert_domain(domain)
                    if ip:
                        insert_ip(ip)

    except Exception as e:
        console.print(f"[red][!] Failed to parse dnsrecon output: {e}[/red]")
