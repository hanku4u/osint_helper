from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.panel import Panel

console = Console()

def metadata_menu():
    console.clear()
    console.print(Panel("🖼️ Metadata Analysis", style="bold green"))
    console.print("1. ExifTool")
    console.print("2. Binwalk")
    console.print("3. Back")

    choice = IntPrompt.ask("\nSelect a tool", choices=["1", "2", "3"])
    if choice == 3:
        return
    console.print(f"\n[italic yellow]Selected tool placeholder: {choice}[/italic yellow]")
    Prompt.ask("Press Enter to return")
