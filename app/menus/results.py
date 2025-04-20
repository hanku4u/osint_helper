from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

console = Console()

def load_results_menu():
    console.clear()
    console.print(Panel("📂 Load Results / View Past Data", style="bold green"))
    console.print("[italic yellow]This feature will be added soon.[/italic yellow]")
    Prompt.ask("Press Enter to return")
