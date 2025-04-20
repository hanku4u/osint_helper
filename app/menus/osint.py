from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.panel import Panel
import os
from runners import run_theharvester, run_spiderfoot_webui

console = Console()

def check_api_key(tool_name, env_var):
    """
    Check if the API key for a tool is set in the environment.
    If not, prompt the user to provide one.
    """
    api_key = os.getenv(env_var)
    if not api_key:
        console.print(f"[bold red]{tool_name} requires an API key.[/bold red]")
        provide_key = Prompt.ask("Would you like to provide an API key now? (y/N)", default="N").lower()
        if provide_key == "y":
            api_key = Prompt.ask(f"Enter your API key for {tool_name}")
            os.environ[env_var] = api_key  # Temporarily set the API key in the environment
            console.print(f"[bold green]API key for {tool_name} set successfully![/bold green]")
        else:
            console.print(f"[bold yellow]Skipping {tool_name} due to missing API key.[/bold yellow]")
            return None
    return api_key

def run_theharvester(session_manager):
    console.print("[bold blue]Running theHarvester...[/bold blue]")
    domain = Prompt.ask("Enter the domain to search")
    console.print(f"[italic yellow]Executing theHarvester for domain: {domain}[/italic yellow]")
    run_theharvester(domain, session_manager)

def run_spiderfoot(session_manager):
    console.print("[bold blue]Running SpiderFoot...[/bold blue]")
    console.print(f"[italic yellow]Opening SpiderFoot Web UI...[/italic yellow]")
    run_spiderfoot_webui(session_manager)

def run_reconng():
    console.print("[bold blue]Running Recon-ng...[/bold blue]")
    workspace = Prompt.ask("Enter the workspace name")
    console.print(f"[italic yellow]Setting up Recon-ng workspace: {workspace}[/italic yellow]")
    # Add the actual execution logic here

def osint_tools_menu(session_manager):
    while True:
        console.clear()
        console.print(Panel("🧠 OSINT Tools", style="bold green"))
        console.print("1. theHarvester")
        console.print("2. SpiderFoot")
        console.print("3. Recon-ng")
        console.print("4. Back")

        choice = IntPrompt.ask("\nSelect a tool")
        if choice == 1:
            run_theharvester(session_manager)
        elif choice == 2:
            run_spiderfoot(session_manager)
        elif choice == 3:
            run_reconng()
        elif choice == 4:
            return
        Prompt.ask("\nPress Enter to return to the OSINT Tools menu")
