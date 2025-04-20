import subprocess
import os
from datetime import datetime
import questionary
from rich.console import Console
from rich.prompt import Prompt
from result_viewer import select_from_result_pool

console = Console()

def run_dnsrecon(session_manager):
    targets = select_from_result_pool(session_manager, "subdomains")
    if not targets:
        console.print("[yellow]No subdomains found. Falling back to domains.[/yellow]")
        targets = select_from_result_pool(session_manager, "domains")

    if not targets:
        console.print("[red]No domains or subdomains available to scan.[/red]")
        return

    args = Prompt.ask("Enter any additional dnsrecon arguments", default="-t std")
    output_dir = session_manager.get_output_path_for_tool("dnsrecon")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    for domain in targets:
        base_filename = f"dnsrecon_{domain.replace('.', '_')}_{timestamp}.txt"
        output_path = os.path.join(output_dir, base_filename)

        cmd = ["dnsrecon", "-d", domain] + args.split()
        console.print(f"[bold green]Running:[/bold green] {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            with open(output_path, "w") as f:
                f.write(result.stdout)

            console.print(f"[green]Results saved to:[/green] {output_path}")

            session_manager.add_tool_run(
                tool_name="dnsrecon",
                input_value=domain,
                output_file=os.path.basename(output_path),
                parsed_file=None
            )
        except subprocess.CalledProcessError as e:
            console.print(f"[red]Error running dnsrecon on {domain}[/red]")
            with open(output_path, "w") as f:
                f.write(e.stdout or "")
                f.write(e.stderr or "")


def run_amass(session_manager):
    targets = select_from_result_pool(session_manager, "subdomains")
    if not targets:
        console.print("[yellow]No subdomains found. Falling back to domains.[/yellow]")
        targets = select_from_result_pool(session_manager, "domains")

    if not targets:
        console.print("[red]No domains or subdomains available to scan.[/red]")
        return

    args = Prompt.ask("Enter any additional amass arguments", default="enum")
    output_dir = session_manager.get_output_path_for_tool("amass")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    for domain in targets:
        base_filename = f"amass_{domain.replace('.', '_')}_{timestamp}.txt"
        output_path = os.path.join(output_dir, base_filename)

        cmd = ["amass"] + args.split() + ["-d", domain]
        console.print(f"[bold green]Running:[/bold green] {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            with open(output_path, "w") as f:
                f.write(result.stdout)

            console.print(f"[green]Results saved to:[/green] {output_path}")

            session_manager.add_tool_run(
                tool_name="amass",
                input_value=domain,
                output_file=os.path.basename(output_path),
                parsed_file=None
            )
        except subprocess.CalledProcessError as e:
            console.print(f"[red]Error running amass on {domain}[/red]")
            with open(output_path, "w") as f:
                f.write(e.stdout or "")
                f.write(e.stderr or "")


def run_fierce(session_manager):
    targets = select_from_result_pool(session_manager, "subdomains")
    if not targets:
        console.print("[yellow]No subdomains found. Falling back to domains.[/yellow]")
        targets = select_from_result_pool(session_manager, "domains")

    if not targets:
        console.print("[red]No domains or subdomains available to scan.[/red]")
        return

    args = Prompt.ask("Enter any additional fierce arguments", default="")
    output_dir = session_manager.get_output_path_for_tool("fierce")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    for domain in targets:
        base_filename = f"fierce_{domain.replace('.', '_')}_{timestamp}.txt"
        output_path = os.path.join(output_dir, base_filename)

        cmd = ["fierce", "-dns", domain] + args.split()
        console.print(f"[bold green]Running:[/bold green] {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            with open(output_path, "w") as f:
                f.write(result.stdout)

            console.print(f"[green]Results saved to:[/green] {output_path}")

            session_manager.add_tool_run(
                tool_name="fierce",
                input_value=domain,
                output_file=os.path.basename(output_path),
                parsed_file=None
            )
        except subprocess.CalledProcessError as e:
            console.print(f"[red]Error running fierce on {domain}[/red]")
            with open(output_path, "w") as f:
                f.write(e.stdout or "")
                f.write(e.stderr or "")


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
