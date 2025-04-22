import subprocess
from app.utils.db import insert_data

def run_whois(domain):
    result = subprocess.run(
        ["whois", domain],
        capture_output=True,
        text=True
    )
    with open(f"results/whois_{domain}.txt", "w") as f:
        f.write(result.stdout)
    parse_and_store(result.stdout)

def parse_and_store(output):
    whois_data = []  # Extract WHOIS key-value pairs from output
    # Parsing logic here...
    insert_data("whois_data", whois_data)
