import sys
import os
import subprocess
import importlib
from rich.console import Console
from rich.prompt import Confirm

console = Console()

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

            # ✅ Prevent infinite loop
            if os.environ.get("OSINT_RESTARTED") != "1":
                console.print("[bold blue]Restarting application...[/bold blue]")
                os.environ["OSINT_RESTARTED"] = "1"
                subprocess.check_call([sys.executable, sys.argv[0]], env=os.environ)
                sys.exit(0)
            else:
                console.print("[yellow]Already restarted once. Skipping auto-restart.[/yellow]")

        except subprocess.CalledProcessError:
            console.print("[red]Failed to install dependencies. Please install manually.[/red]")
            sys.exit(1)
    else:
        console.print("[red]Cannot continue without required packages.[/red]")
        sys.exit(1)
