import re

def parse_theharvester_output(output, session_manager):
    """
    Parses theHarvester output and updates the session with subdomains and IPs.
    """
    subdomains = set()
    ips = set()

    # Example regex to extract subdomains and IPs
    subdomain_pattern = re.compile(r"(?P<subdomain>[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})")
    ip_pattern = re.compile(r"(?P<ip>\b\d{1,3}(\.\d{1,3}){3}\b)")

    for line in output.splitlines():
        # Extract subdomains
        subdomain_match = subdomain_pattern.search(line)
        if subdomain_match:
            subdomain = subdomain_match.group("subdomain")
            subdomains.add(subdomain)

        # Extract IPs
        ip_match = ip_pattern.search(line)
        if ip_match:
            ip = ip_match.group("ip")
            ips.add(ip)

    # Add subdomains and IPs to the session
    for subdomain in subdomains:
        session_manager.add_to_pool("subdomains", subdomain)

    for ip in ips:
        session_manager.add_to_pool("ips", ip)

    print(f"Added {len(subdomains)} subdomains and {len(ips)} IPs to the session.")