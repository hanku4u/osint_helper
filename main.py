from textual.app import App
from textual.widgets import Button, Header, Footer, Static

from app.tools.harvester_runner import run_theharvester
from app.tools.dns_runner import run_dnsrecon
from app.tools.whois_runner import run_whois
from app.tools.nmap_runner import run_nmap
from app.reporting.report_generator import generate_report
from app.ui.session_view import SessionReview
from app.utils.db import fetch_data

class MainMenu(App):
    def compose(self):
        yield Header()
        yield Static("OSINT CLI Toolkit", id="title")
        yield Button("Run theHarvester", id="harvester")
        yield Button("Run DNS Enumeration", id="dns")
        yield Button("Run WHOIS Lookup", id="whois")
        yield Button("Run Nmap Scan", id="nmap")
        yield Button("Review Current Session Data", id="review")
        yield Button("Export Report", id="export")
        yield Button("Exit", id="exit")
        yield Footer()

    def on_button_pressed(self, event):
        button_id = event.button.id
        if button_id == "exit":
            self.exit()
        elif button_id == "harvester":
            run_theharvester("example.com")  # Replace with dynamic domain input
        elif button_id == "dns":
            run_dnsrecon("example.com")  # Replace with dynamic domain input
        elif button_id == "whois":
            run_whois("example.com")  # Replace with dynamic domain input
        elif button_id == "nmap":
            run_nmap("example.com")  # Replace with dynamic domain input
        elif button_id == "review":
            if not any(fetch_data(table) for table in ["emails", "domains", "subdomains", "ips", "dns_records", "whois_data", "nmap_results"]):
                self.mount(Static("No session data available."))
            else:
                self.mount(SessionReview())  # Open session review panel
        elif button_id == "export":
            generate_report()

if __name__ == "__main__":
    MainMenu().run()