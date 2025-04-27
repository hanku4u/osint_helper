# app/tools/dns_runner.py

import subprocess
import datetime
import os
import json
from rich.console import Console
from app.db.session_db import (
    insert_ip,
    insert_a_record,
    insert_ns_record,
    insert_mx_record,
    insert_txt_record,
    insert_srv_record,
    insert_soa_record
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
    """Parse dnsrecon JSON output and insert all record types into session database."""
    try:
        if not os.path.exists(filepath):
            console.print(f"[red][!] JSON output file not found: {filepath}[/red]")
            return

        with open(filepath, "r") as file:
            data = json.load(file)

        for record in data:
            # Ignore scan metadata
            if record.get("type", "").lower() == "scaninfo":
                continue

            record_type = record.get("type", "").upper()

            if record_type == "A":
                insert_a_record(
                    record.get("name"),
                    record.get("domain"),
                    record.get("address")
                )

            elif record_type == "NS":
                insert_ns_record(
                    record.get("domain"),
                    record.get("target"),
                    record.get("address"),
                    record.get("recursive"),
                    record.get("Version")
                )

            elif record_type == "MX":
                insert_mx_record(
                    record.get("domain"),
                    record.get("exchange"),
                    record.get("address")
                )

            elif record_type == "TXT":
                insert_txt_record(
                    record.get("domain"),
                    record.get("name"),
                    record.get("strings")
                )

            elif record_type == "SRV":
                insert_srv_record(
                    record.get("domain"),
                    record.get("name"),
                    record.get("target"),
                    record.get("port"),
                    record.get("address")
                )

            elif record_type == "SOA":
                insert_soa_record(
                    record.get("domain"),
                    record.get("mname"),
                    record.get("address")
                )

            # ✅ Insert into ips table if address exists (even if record type is not "A")
            address = record.get("address")
            if address:
                insert_ip(address)

    except Exception as e:
        console.print(f"[red][!] Failed to parse dnsrecon JSON output: {e}[/red]")
