# runners/theharvester_runner.py

import subprocess
import os
from datetime import datetime
from rich.console import Console

console = Console()

def run_theharvester(domain, session_manager):
    output_dir = session_manager.get_output_path_for_tool("theHarvester")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    base_filename = f"theharvester_{domain}_{timestamp}"
    output_path = os.path.join(output_dir, f"{base_filename}.txt")

    # Build command
    cmd = [
        "theHarvester",
        "-d", domain,
        "-b", "all",
        "-f", os.path.join(output_dir, base_filename)
    ]

    console.print(f"[bold green]Executing:[/bold green] {' '.join(cmd)}")

    try:
        # Run theHarvester
        subprocess.run(cmd, check=True)
        console.print(f"[green]Results saved to:[/green] {output_path}")

        # Update session
        session_manager.add_tool_run(
            tool_name="theHarvester",
            input_value=domain,
            output_file=f"{base_filename}.txt"
        )

        # TODO: parse output and update result pool here

    except subprocess.CalledProcessError:
        console.print(f"[bold red]Error:[/bold red] Failed to run theHarvester on {domain}")
