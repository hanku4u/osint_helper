# runners/spiderfoot_runner.py

import subprocess
import webbrowser
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def run_spiderfoot_webui(session_manager=None):
    console.print("[green]Starting SpiderFoot Web UI on [bold]127.0.0.1:80[/bold]...[/green]")

    try:
        subprocess.Popen(["spiderfoot", "-l", "127.0.0.1:80"])
        console.print("[bold green]SpiderFoot server started successfully.[/bold green]")
    except FileNotFoundError:
        console.print("[bold red]Error:[/bold red] 'spiderfoot' command not found. Is it installed and in your PATH?")
        return
    except Exception as e:
        console.print(f"[bold red]Failed to start SpiderFoot:[/bold red] {e}")
        return

    # Open Firefox to the UI
    try:
        webbrowser.get("firefox").open("http://127.0.0.1:80")
    except webbrowser.Error:
        console.print("[yellow]Could not open Firefox. Trying the default browser instead...[/yellow]")
        webbrowser.open("http://127.0.0.1:80")

    Prompt.ask("\n[dim]Press Enter to return to the OSINT Tools menu[/dim]")
