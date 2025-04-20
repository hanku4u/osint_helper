import subprocess
import os
from datetime import datetime
import questionary
from rich.console import Console
from rich.prompt import Prompt
from result_viewer import select_from_result_pool

console = Console()

def run_dns_tool(session_manager, tool_name, base_cmd, default_args):
    targets = select_from_result_pool(session_manager, "subdomains") or select_from_result_pool(session_manager, "domains")
    if not targets:
        console.print(f"[red]No domains or subdomains available to scan for {tool_name}.[/red]")
        return

    args = Prompt.ask(f"Enter any additional {tool_name} arguments", default=default_args)
    output_dir = session_manager.get_output_path_for_tool(tool_name)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    for domain in targets:
        base_filename = f"{tool_name}_{domain.replace('.', '_')}_{timestamp}.txt"
        output_path = os.path.join(output_dir, base_filename)

        cmd = base_cmd + args.split() + ["-d", domain]
        console.print(f"[bold green]Running:[/bold green] {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            with open(output_path, "w") as f:
                f.write(result.stdout)

            console.print(f"[green]Results saved to:[/green] {output_path}")

            session_manager.add_tool_run(
                tool_name=tool_name,
                input_value=domain,
                output_file=os.path.basename(output_path),
                parsed_file=None
            )
        except subprocess.CalledProcessError as e:
            console.print(f"[red]Error running {tool_name} on {domain}[/red]")
            with open(output_path, "w") as f:
                f.write(e.stdout or "")
                f.write(e.stderr or "")

def run_dnsrecon(session_manager):
    run_dns_tool(session_manager, "dnsrecon", ["dnsrecon"], "-t std")

def run_amass(session_manager):
    run_dns_tool(session_manager, "amass", ["amass", "enum"], "")

def run_fierce(session_manager):
    run_dns_tool(session_manager, "fierce", ["fierce", "-dns"], "")

def dns_tools_menu(session):
    while True:
        choice = questionary.select(
            "Choose a DNS/Subdomain enumeration tool:",
            choices=[
                "dnsrecon",
                "amass",
                "fierce",
                "Back"
            ]
        ).ask()

        if choice == "dnsrecon":
            run_dnsrecon(session)
        elif choice == "amass":
            run_amass(session)
        elif choice == "fierce":
            run_fierce(session)
        elif choice == "Back":
            break
