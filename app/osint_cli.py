from env_check import check_environment
check_environment()

from rich.console import Console
from rich.prompt import IntPrompt
from rich.panel import Panel
import sys

# Import menu functions
from menus.osint import osint_tools_menu
from menus.domain import domain_menu
from menus.people import people_menu
from menus.infrastructure import infrastructure_menu
from menus.metadata import metadata_menu
from menus.results import load_results_menu

console = Console()

def print_header(title: str):
    console.clear()
    console.print(Panel(title, expand=False, style="bold green"))

def main_menu():
    while True:
        print_header("🔧 OSINT Toolkit - Main Menu")
        console.print("[bold]Select a category:[/bold]\n")
        console.print("1. OSINT Tools")
        console.print("2. Domain & Subdomain Recon")
        console.print("3. Email & People Search")
        console.print("4. Infrastructure Scanning")
        console.print("5. Metadata Analysis")
        console.print("6. Load Results / View Past Data")
        console.print("7. Quit")

        choice = IntPrompt.ask("\nSelect a menu")

        if choice == 1:
            osint_tools_menu()
        elif choice == 2:
            domain_menu()
        elif choice == 3:
            people_menu()
        elif choice == 4:
            infrastructure_menu()
        elif choice == 5:
            metadata_menu()
        elif choice == 6:
            load_results_menu()
        elif choice == 7:
            console.print("\n[bold red]Goodbye![/bold red]")
            sys.exit()

if __name__ == "__main__":
    main_menu()
