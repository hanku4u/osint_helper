import subprocess
from app.utils.db import insert_data

def run_dnsrecon(domain):
    result = subprocess.run(
        ["dnsrecon", "-d", domain],
        capture_output=True,
        text=True
    )
    with open(f"results/dnsrecon_{domain}.txt", "w") as f:
        f.write(result.stdout)
    parse_and_store(result.stdout)

def parse_and_store(output):
    dns_records = []  # Extract DNS records from output
    # Parsing logic here...
    insert_data("dns_records", dns_records)
