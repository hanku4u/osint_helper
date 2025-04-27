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

    # Base default arguments
    base_args = [
        "-d", domain,
        "-b", "all",
        "-l", "100",
    ]

    # Merge user arguments if any
    user_args = custom_args.split() if custom_args else []

    # If user overrides defaults (e.g., supplies -l), replace
    final_args = []
    skip_next = False
    forbidden_args = ["-d", "-b", "-l"]

    # Build a map of user args for easy checking
    user_args_map = {}
    i = 0
    while i < len(user_args):
        if user_args[i].startswith("-"):
            key = user_args[i]
            value = None
            if (i + 1) < len(user_args) and not user_args[i+1].startswith("-"):
                value = user_args[i+1]
                i += 1
            user_args_map[key] = value
        i += 1

    # Rebuild base_args, skipping if user provided override
    i = 0
    while i < len(base_args):
        key = base_args[i]
        if key in forbidden_args and key in user_args_map:
            # User overrode this argument
            i += 2  # skip value too
            continue
        final_args.append(key)
        if (i + 1) < len(base_args):
            final_args.append(base_args[i+1])
        i += 2

    # Add user-supplied args at the end
    for key, value in user_args_map.items():
        final_args.append(key)
        if value:
            final_args.append(value)

    # Final command
    command = ["theHarvester"] + final_args

    try:
        full_command_str = " ".join(command)

        with console.status(f"[bold green]Running: {full_command_str}[/bold green]", spinner="dots"):
            # Capture output
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

        # Save all output to file
        with open(output_path, "w") as output_file:
            output_file.write(result.stdout)

        # If error happened
        if result.returncode != 0:
            console.print(f"[red][!] theHarvester returned an error (exit code {result.returncode}):[/red]")
            console.print(result.stdout)
            return ""

    except Exception as e:
        console.print(f"[red][!] Unexpected error running theHarvester: {e}[/red]")
        return ""

    return output_path
