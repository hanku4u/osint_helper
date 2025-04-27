# app/tools/dns_runner.py

import subprocess
import datetime
import os
import json
from rich.console import Console
from app.db.session_db import (
    insert_domain,
    insert_ip,
    insert_txt_record,
    insert_srv_record
)

console = Console()

RESULTS_DIR = "results"

def run_dnsrecon(domain: str, custom_args: str = "") -> str:
    """Run dnsrecon on a domain, parse JSON output, and store results."""
    os.makedirs(RESULTS_DIR, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_json_filename = f"dnsrecon_{domain}_{timestamp}.json"
    output_json_path = os.path.join(RESULTS_DIR, output_json_filename)

    # Always add -j <output_file> to force JSON output
    base_args = [
        "-d", domain,
        "-j", output_json_path
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

        if result.returncode != 0:
            console.print(f"[red][!] dnsrecon returned an error (exit code {result.returncode}):[/red]")
            console.print(result.stdout)
            return ""

        # ✅ Parse the JSON output now
        parse_and_store_dnsrecon_json(output_json_path)

    except Exception as e:
        console.print(f"[red][!] Unexpected error running dnsrecon: {e}[/red]")
        return ""

    return output_json_path

def parse_and_store_dnsrecon_json(filepath):
    """Parse dnsrecon JSON output and insert found domains/IPs/TXT/SRV records into the session database."""
    try:
        if not os.path.exists(filepath):
            console.print(f"[red][!] JSON output file not found: {filepath}[/red]")
            return

        with open(filepath, "r") as file:
            data = json.load(file)

        for record in data:
            record_type = record.get("type", "").upper()

            if record_type == "A":
                domain = record.get("name")
                ip = record.get("address")
                if domain:
                    insert_domain(domain)
                if ip:
                    insert_ip(ip)

            elif record_type == "TXT":
                domain = record.get("domain")
                name = record.get("name")
                value = record.get("strings")
                if domain and name and value:
                    insert_txt_record(domain, name, value)

            elif record_type == "SRV":
                domain = record.get("domain")
                name = record.get("name")
                target = record.get("target")
                port = record.get("port")
                address = record.get("address")
                if domain and name and target and port:
                    insert_srv_record(domain, name, target, port, address)

            # (Optional) Handle other types (NS, MX, etc.) later if needed

    except Exception as e:
        console.print(f"[red][!] Failed to parse dnsrecon JSON output: {e}[/red]")
