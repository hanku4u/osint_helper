# app/tools/harvester_runner.py

import subprocess
import datetime
import os

RESULTS_DIR = "results"

def run_theharvester(domain: str, custom_args: str = "") -> str:
    """Run theHarvester with the given domain and optional custom arguments.
    
    Args:
        domain (str): The domain or IP to target.
        custom_args (str, optional): Extra command-line arguments.

    Returns:
        str: Path to the output file containing raw theHarvester results.
    """
    # Ensure results directory exists
    os.makedirs(RESULTS_DIR, exist_ok=True)

    # Create a unique filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"theharvester_{domain}_{timestamp}.txt"
    output_path = os.path.join(RESULTS_DIR, output_filename)

    # Build theHarvester command
    command = [
        "theHarvester",
        "-d", domain,
        "-b", "all",  # Default source is "all"
    ]

    # Append any custom arguments provided by user
    if custom_args:
        command += custom_args.split()

    try:
        with open(output_path, "w") as output_file:
            subprocess.run(command, stdout=output_file, stderr=subprocess.STDOUT, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[!] Error running theHarvester: {e}")
        return ""

    return output_path
