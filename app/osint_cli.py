# osint_cli.py

from env_check import check_environment

# Check environment before importing third-party packages
check_environment()

# Now import everything else
from session_manager import SessionManager
from harvest_runner import run_theharvester
from result_viewer import (
    review_results,
    view_nmap_services,
    view_dns_results,
    view_searchsploit_results,
    view_shodan_results
)
from report_exporter import export_session_report
from tools.dns_tools import dns_tools_menu
from tools.nmap_tool import run_nmap
from tools.searchsploit_tool import run_searchsploit
from tools.shodan_tool import run_shodan

import questionary
from rich.console import Console

console = Console()

def select_option(message: str, options: list[str]) -> str:
    return questionary.select(message, choices=options).ask()

def tools_menu(session):
    while True:
        choice = select_option("Choose a post-harvest tool to run:", [
            "DNS & Subdomain Enumeration",
            "Nmap",
            "Searchsploit",
            "Shodan",
            "View Results",
            "Export Report",
            "Exit"
        ])

        if choice == "DNS & Subdomain Enumeration":
            dns_tools_menu(session)
        elif choice == "Nmap":
            run_nmap(session)
        elif choice == "Searchsploit":
            run_searchsploit(session)
        elif choice == "Shodan":
            run_shodan(session)
        elif choice == "View Results":
            view_results_menu(session)
        elif choice == "Export Report":
            export_session_report(session)
        elif choice == "Exit":
            console.print("\n[bold red]Goodbye![/bold red]")
            break

def view_results_menu(session):
    while True:
        choice = select_option("What would you like to view?", [
            "theHarvester Results",
            "Nmap Discovered Services",
            "DNS Tool Outputs",
            "Searchsploit Results",
            "Shodan Results",
            "Back"
        ])

        if choice == "theHarvester Results":
            review_results(session)
        elif choice == "Nmap Discovered Services":
            view_nmap_services(session)
        elif choice == "DNS Tool Outputs":
            view_dns_results(session)
        elif choice == "Searchsploit Results":
            view_searchsploit_results(session)
        elif choice == "Shodan Results":
            view_shodan_results(session)
        elif choice == "Back":
            break

def main():
    session = SessionManager()
    session.init_session()

    run_theharvester(session)
    review_results(session)
    tools_menu(session)

if __name__ == "__main__":
    main()
