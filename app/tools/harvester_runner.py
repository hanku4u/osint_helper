# app/tools/harvester_runner.py

import subprocess
import datetime
import os
from rich.console import Console

console = Console()

RESULTS_DIR = "results"

def run_theharvester(domain: str, custom_args: str = "") -> str:
    """Run theHarvester with the given domain and optional custom arguments."""
    os.makedirs(RESULTS_DIR, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"theharvester_{domain}_{timestamp}.txt"
    output_path = os.path.join(RESULTS_DIR, output_filename)

    # Build default command
    command = [
        "theHarvester",
        "-d", domain,
        "-b", "all",
        "-l", "100",
    ]

    # Add user arguments (they can override defaults)
    if custom_args:
        command += custom_args.split()

    try:
        with console.status("[bold green]Running theHarvester...[/bold green]", spinner="dots"):
            # Run and capture output in memory first
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

        # Always save the output to file
        with open(output_path, "w") as output_file:
            output_file.write(result.stdout)

        # Check exit code
        if result.returncode != 0:
            console.print(f"[red][!] theHarvester returned an error (exit code {result.returncode}):[/red]")
            console.print(result.stdout)  # Show theHarvester's output immediately
            return ""

    except Exception as e:
        console.print(f"[red][!] Unexpected error running theHarvester: {e}[/red]")
        return ""

    return output_path
