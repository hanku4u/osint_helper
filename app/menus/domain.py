from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.panel import Panel

console = Console()

def domain_menu():
    console.clear()
    console.print(Panel("🌐 Domain & Subdomain Recon", style="bold green"))
    console.print("1. Sublist3r")
    console.print("2. dnsenum")
    console.print("3. Amass")
    console.print("4. Back")

    choice = IntPrompt.ask("\nSelect a tool", choices=["1", "2", "3", "4"])
    if choice == 4:
        return
    console.print(f"\n[italic yellow]Selected tool placeholder: {choice}[/italic yellow]")
    Prompt.ask("Press Enter to return")
