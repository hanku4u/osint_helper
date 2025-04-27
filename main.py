# main.py

from startup import environment_check
from app.cli import main_menu
from app.db.session_db import set_db_path, initialize_database
from rich.console import Console
from rich.prompt import Prompt
import os

console = Console()

def select_or_create_session():
    console.print("[bold cyan]Welcome to OSINT CLI Toolkit[/bold cyan]")
    console.print("[1] Start New Session")
    console.print("[2] Load Previous Session")

    choice = Prompt.ask("Choose an option", choices=["1", "2"])

    if choice == "1":
        set_db_path()  # Create a fresh session
        initialize_database()
        console.print("[green]New session started.[/green]")
    elif choice == "2":
        db_files = [f for f in os.listdir("sessions") if f.endswith(".db")]
        if not db_files:
            console.print("[red]No previous sessions found. Starting new session.[/red]")
            set_db_path()
            initialize_database()
            return

        console.print("\nAvailable Sessions:")
        for idx, dbfile in enumerate(db_files, 1):
            console.print(f"[{idx}] {dbfile}")

        selection = Prompt.ask("Select a session number", choices=[str(i) for i in range(1, len(db_files)+1)])
        selected_file = db_files[int(selection)-1]
        set_db_path(selected_file)
        console.print(f"[green]Loaded session: {selected_file}[/green]")


if __name__ == "__main__":
    environment_check()
    select_or_create_session()
    main_menu()
