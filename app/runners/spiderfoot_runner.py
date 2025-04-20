import subprocess
import webbrowser
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def run_spiderfoot_webui(session_manager=None):
    console.print("[green]Starting SpiderFoot Web UI on [bold]http://127.0.0.1:80[/bold]...[/green]")

    try:
        subprocess.Popen(["spiderfoot", "-l", "127.0.0.1:80"])
        console.print("[bold green]SpiderFoot server started successfully.[/bold green]")
    except FileNotFoundError:
        console.print("[bold red]Error:[/bold red] 'spiderfoot' command not found. Is it installed and in your PATH?")
        return
    except Exception as e:
        console.print(f"[bold red]Failed to start SpiderFoot:[/bold red] {e}")
        return

    url = "http://127.0.0.1"

    # Explicitly launch Firefox with HTTP
    try:
        subprocess.Popen(["firefox", url])
        console.print(f"[green]Firefox opened at {url}[/green]")
    except FileNotFoundError:
        console.print("[yellow]Firefox not found. Trying default system browser instead...[/yellow]")
        webbrowser.open(url)

    Prompt.ask("\n[dim]Press Enter to return to the OSINT Tools menu[/dim]")
