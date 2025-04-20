from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.panel import Panel

console = Console()

def osint_tools_menu():
    console.clear()
    console.print(Panel("🧠 OSINT Tools", style="bold green"))
    console.print("1. theHarvester")
    console.print("2. SpiderFoot")
    console.print("3. Recon-ng")
    console.print("4. Back")

    choice = IntPrompt.ask("\nSelect a tool")
    if choice == 4:
        return
    console.print(f"\n[italic yellow]Selected tool placeholder: {choice}[/italic yellow]")
    Prompt.ask("Press Enter to return")
