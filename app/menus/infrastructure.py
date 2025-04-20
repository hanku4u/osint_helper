from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.panel import Panel

console = Console()

def infrastructure_menu():
    console.clear()
    console.print(Panel("📡 Infrastructure Scanning", style="bold green"))
    console.print("1. Nmap")
    console.print("2. Shodan")
    console.print("3. WhatWeb")
    console.print("4. Back")

    choice = IntPrompt.ask("\nSelect a tool", choices=["1", "2", "3", "4"])
    if choice == 4:
        return
    console.print(f"\n[italic yellow]Selected tool placeholder: {choice}[/italic yellow]")
    Prompt.ask("Press Enter to return")
