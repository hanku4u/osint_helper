import subprocess
from app.utils.db import insert_data

def run_nmap(domain):
    result = subprocess.run(
        ["nmap", "-sV", domain],
        capture_output=True,
        text=True
    )
    with open(f"results/nmap_{domain}.txt", "w") as f:
        f.write(result.stdout)
    parse_and_store(result.stdout)

def parse_and_store(output):
    nmap_results = []  # Extract port, service, and version info from output
    # Parsing logic here...
    insert_data("nmap_results", nmap_results)
