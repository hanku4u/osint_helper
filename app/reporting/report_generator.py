import sqlite3

def generate_report():
    conn = sqlite3.connect("session/session.db")
    cursor = conn.cursor()
    with open("report.md", "w") as md, open("report.txt", "w") as txt:
        # Fetch data and write to reports
        tables = ["emails", "domains", "subdomains", "ips", "dns_records", "whois_data", "nmap_results"]
        for table in tables:
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            md.write(f"## {table.capitalize()}\n")
            txt.write(f"{table.capitalize()}\n")
            for row in rows:
                md.write(f"- {row}\n")
                txt.write(f"- {row}\n")
            md.write("\n")
            txt.write("\n")
    conn.close()