# app/tools/harvester_runner.py

import subprocess
import datetime
import os
import re
from rich.console import Console
from app.db.session_db import (
    insert_target,
    insert_domain,
    insert_email,
    insert_ip,
    insert_host
)

console = Console()

RESULTS_DIR = "results"

def run_theharvester(domain: str, custom_args: str = "") -> str:
    """Run theHarvester, parse output, and store results."""
    os.makedirs(RESULTS_DIR, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"theharvester_{domain}_{timestamp}.txt"
    output_path = os.path.join(RESULTS_DIR, output_filename)

    # Build command
    base_args = [
        "-d", domain,
        "-b", "all",
        "-l", "100",
    ]

    user_args = custom_args.split() if custom_args else []

    user_args_map = {}
    i = 0
    while i < len(user_args):
        if user_args[i].startswith("-"):
            key = user_args[i]
            value = None
            if (i + 1) < len(user_args) and not user_args[i+1].startswith("-"):
                value = user_args[i+1]
                i += 1
            user_args_map[key] = value
        i += 1

    final_args = []
    i = 0
    while i < len(base_args):
        key = base_args[i]
        if key in ["-d", "-b", "-l"] and key in user_args_map:
            i += 2
            continue
        final_args.append(key)
        if (i + 1) < len(base_args):
            final_args.append(base_args[i+1])
        i += 2

    for key, value in user_args_map.items():
        final_args.append(key)
        if value:
            final_args.append(value)

    command = ["theHarvester"] + final_args

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
            console.print(f"[red][!] theHarvester returned an error (exit code {result.returncode}):[/red]")
            console.print(result.stdout)
            return ""

        # ✅ After successful scan, parse the output
        parse_and_store_harvester_output(output_path)

    except Exception as e:
        console.print(f"[red][!] Unexpected error running theHarvester: {e}[/red]")
        return ""

    return output_path

def parse_and_store_harvester_output(filepath):
    """Parse theHarvester text output and insert results into the session database."""
    try:
        with open(filepath, "r") as file:
            lines = file.readlines()

        # Step 1: Ignore first 14 lines (banner)
        lines = lines[14:]

        # Step 2: Join and split on [*] markers
        text = ''.join(lines)
        sections = text.split("[*]")

        email_pattern = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
        ip_pattern = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")

        in_hosts_section = False

        for section in sections:
            section = section.strip()

            if not section:
                continue

            if section.startswith("Target:"):
                target = section.split("Target:")[-1].strip()
                if target:
                    insert_target(target)
                continue

            if section.startswith("Hosts found"):
                in_hosts_section = True
                continue

            if in_hosts_section:
                # Hosts are dumped here after "Hosts found"
                host_lines = section.splitlines()

                # Skip first line if it's just dashes
                if host_lines and set(host_lines[0]) == {"-"}:
                    host_lines = host_lines[1:]

                for host in host_lines:
                    host = host.strip()
                    if "." in host:
                        insert_host(host)

                in_hosts_section = False  # Only process once
                continue

            # Parse other sections for emails and IPs
            for match in email_pattern.findall(section):
                insert_email(match)

            for match in ip_pattern.findall(section):
                insert_ip(match)

    except Exception as e:
        console.print(f"[red][!] Failed to parse harvester output: {e}[/red]")
