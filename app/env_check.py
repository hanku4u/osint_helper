import sys
import subprocess
import importlib
from rich.console import Console
from rich.prompt import Confirm

console = Console()

# Add any new dependencies here
REQUIRED_PACKAGES = [
    "rich",
    "questionary",
    "shodan"
]

def check_environment():
    console.print("[bold cyan]Checking environment...[/bold cyan]")

    missing = []

    for pkg in REQUIRED_PACKAGES:
        try:
            importlib.import_module(pkg)
        except ImportError:
            missing.append(pkg)

    if not missing:
        console.print("[green]All dependencies are satisfied.[/green]")
        return

    console.print(f"[yellow]Missing packages:[/yellow] {', '.join(missing)}")

    if Confirm.ask("Would you like to install them now?", default=True):
        try:
            subprocess.check_call(["pip", "install", *missing])
            console.print("[green]Dependencies installed successfully.[/green]")
        except subprocess.CalledProcessError:
            console.print("[red]Failed to install dependencies. Please install manually.[/red]")
            sys.exit(1)
    else:
        console.print("[red]Cannot continue without required packages.[/red]")
        sys.exit(1)
