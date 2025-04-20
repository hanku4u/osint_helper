# tools/nmap_tool.py

import subprocess
import os
import re
from datetime import datetime
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from result_viewer import select_from_result_pool

console = Console()

def parse_nmap_output(text):
    results = []
    parsing_ports = False

    for line in text.splitlines():
        if re.match(r"PORT\s+STATE\s+SERVICE", line):
            parsing_ports = True
            continue
        if parsing_ports:
            if not line.strip():
                break  # End of port section
            parts = line.split()
            if len(parts) >= 3:
                port_proto = parts[0]      # e.g. 80/tcp
                state = parts[1]           # e.g. open
                service = parts[2]         # e.g. http
                version = " ".join(parts[3:]) if len(parts) > 3 else ""
                if state == "open":
                    results.append((port_proto, service, version))
    return results

def display_port_summary(target, parsed_results):
    if not parsed_results:
        console.print(f"[yellow]No open ports found for {target}[/yellow]")
        return

    table = Table(title=f"🔍 Open Ports for {target}")
    table.add_column("Port", style="cyan")
    table.add_column("Service", style="green")
    table.add_column("Version Info", style="white")

    for port, service, version in parsed_results:
        table.add_row(port, service, version)

    console.print(table)

def run_nmap(session_manager):
    choice = Prompt.ask("Scan [ips] or [subdomains]?", choices=["ips", "subdomains"], default="ips")
    targets = select_from_result_pool(session_manager, choice)

    if not targets:
        return

    args = Prompt.ask("Enter any additional Nmap arguments", default="-sV")

    output_dir = session_manager.get_output_path_for_tool("nmap")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    for target in targets:
        base_filename = f"nmap_{target.replace('.', '_')}_{timestamp}.txt"
        output_path = os.path.join(output_dir, base_filename)

        cmd = ["nmap", *args.split(), target]

        console.print(f"[bold green]Running:[/bold green] {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            output_text = result.stdout

            # Save raw output
            with open(output_path, "w") as f:
                f.write(output_text)

            console.print(f"[green]Scan complete. Results saved to:[/green] {output_path}")

            # Parse and display
            parsed = parse_nmap_output(output_text)
            display_port_summary(target, parsed)

            # Save parsed results to session
            service_entries = [
                {
                    "target": target,
                    "port": port,
                    "service": service,
                    "version": version
                }
                for (port, service, version) in parsed
            ]
            session_manager.update_result_pool("nmap_services", service_entries)

            session_manager.add_tool_run(
                tool_name="nmap",
                input_value=target,
                output_file=os.path.basename(output_path),
                parsed_file=None
            )

        except subprocess.CalledProcessError as e:
            console.print(f"[red]Error running Nmap on {target}[/red]")
            with open(output_path, "w") as f:
                f.write(e.stdout or "")
                f.write(e.stderr or "")
