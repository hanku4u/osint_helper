# app/tools/harvester_runner.py

import subprocess
import datetime
import os

RESULTS_DIR = "results"

def run_theharvester(domain: str, custom_args: str = "") -> str:
    """Run theHarvester with the given domain and optional custom arguments."""
    os.makedirs(RESULTS_DIR, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"theharvester_{domain}_{timestamp}.txt"
    output_path = os.path.join(RESULTS_DIR, output_filename)

    command = [
        "theHarvester",
        "-d", domain,
        "-b", "all",
    ]

    if custom_args:
        command += custom_args.split()

    try:
        with open(output_path, "w") as output_file:
            subprocess.run(command, stdout=output_file, stderr=subprocess.STDOUT, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[!] Error running theHarvester: {e}")
        return ""

    return output_path
