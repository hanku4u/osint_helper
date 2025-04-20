import subprocess
import time
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def run_spiderfoot_webui(session_manager=None):
    console.print("[green]Starting SpiderFoot Web UI on [bold]http://127.0.0.1:80[/bold]...[/green]")

    try:
        subprocess.Popen(["spiderfoot", "-l", "127.0.0.1:80"])
        time.sleep(3)  # Allow server to initialize
    except FileNotFoundError:
        console.print("[bold red]Error:[/bold red] 'spiderfoot' command not found.")
        return
    except Exception as e:
        console.print(f"[bold red]Failed to start SpiderFoot:[/bold red] {e}")
        return

    try:
        subprocess.Popen(["firefox", "--new-window", "http://127.0.0.1:80"])
        console.print("[green]Opened Firefox to [bold]http://127.0.0.1:80[/bold][/green]")
    except FileNotFoundError:
        console.print("[yellow]Firefox not found. Trying default browser instead...[/yellow]")
        import webbrowser
        webbrowser.open("http://127.0.0.1:80")

    Prompt.ask("\n[dim]Press Enter to return to the OSINT Tools menu[/dim]")
