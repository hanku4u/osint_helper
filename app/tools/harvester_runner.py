import subprocess
from app.utils.db import insert_data

def run_theharvester(domain, harvester_path="theHarvester"):
    try:
        result = subprocess.run(
            [harvester_path, "-d", domain, "-b", "all"],
            capture_output=True,
            text=True
        )
        with open(f"results/theharvester_{domain}.txt", "w") as f:
            f.write(result.stdout)
        parse_and_store(result.stdout)
    except FileNotFoundError:
        print(f"Error: '{harvester_path}' not found. Ensure it is installed and in your PATH.")
        return

def parse_and_store(output):
    emails = set()  # Extract emails from output
    domains = set()  # Extract domains from output
    # Parsing logic here...
    insert_data("emails", emails)
    insert_data("domains", domains)
