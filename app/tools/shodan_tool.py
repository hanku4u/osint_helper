# tools/shodan_tool.py

import os
import shodan
from datetime import datetime
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from result_viewer import select_from_result_pool

console = Console()

def run_shodan(session_manager):
    api_key = os.getenv("SHODAN_API_KEY")
    if not api_key:
        console.print("[yellow]No SHODAN_API_KEY found in your environment.[/yellow]")
        api_key = Prompt.ask("Enter your Shodan API key")
        os.environ["SHODAN_API_KEY"] = api_key

    api = shodan.Shodan(api_key)

    choice = Prompt.ask("Scan [ips] from previous tools or enter manually?", choices=["ips", "manual"], default="ips")

    if choice == "ips":
        targets = select_from_result_pool(session_manager, "ips")
    else:
        ip = Prompt.ask("Enter a single IP address")
        targets = [ip] if ip else []

    if not targets:
        console.print("[red]No IPs selected or entered.[/red]")
        return

    output_dir = session_manager.get_output_path_for_tool("shodan")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    for ip in targets:
        base_filename = f"shodan_{ip.replace('.', '_')}_{timestamp}.json"
        output_path = os.path.join(output_dir, base_filename)

        try:
            host = api.host(ip)

            with open(output_path, "w") as f:
                import json
                json.dump(host, f, indent=2)

            console.print(f"[green]Results saved to:[/green] {output_path}")

            # Display summary
            table = Table(title=f"📡 Shodan Info for {ip}")
            table.add_column("Field", style="cyan")
            table.add_column("Value", style="white")

            table.add_row("IP", str(host.get("ip_str", "")))
            table.add_row("Org", str(host.get("org", "N/A")))
            table.add_row("ISP", str(host.get("isp", "N/A")))
            table.add_row("Hostnames", ", ".join(host.get("hostnames", [])))
            table.add_row("Ports", ", ".join(map(str, host.get("ports", []))))
            table.add_row("Country", host.get("country_name", ""))
            table.add_row("City", host.get("city", ""))

            console.print(table)

            session_manager.add_tool_run(
                tool_name="shodan",
                input_value=ip,
                output_file=os.path.basename(output_path),
                parsed_file=None
            )

        except shodan.APIError as e:
            console.print(f"[red]Error querying Shodan for {ip}: {e}[/red]")
