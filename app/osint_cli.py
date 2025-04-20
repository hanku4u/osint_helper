from rich.console import Console
import questionary
from env_check import check_environment
from session_manager import SessionManager
from harvest_runner import run_theharvester
from tools import dns_tools_menu, run_nmap, run_searchsploit, run_shodan
from result_viewer import *
from report_exporter import export_session_report

console = Console()

def select_option(message: str, options: list[str]) -> str:
    return questionary.select(message, choices=options).ask()

def view_results_menu(session):
    while True:
        choice = select_option("What would you like to view?", [
            "theHarvester Results",
            "Nmap Discovered Services",
            "DNS Tool Outputs",
            "Searchsploit Results",
            "Shodan Results",
            "Export Session Report",
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
        elif choice == "Export Session Report":
            export_session_report(session)
        elif choice == "Back":
            break

def tools_menu(session):
    while True:
        choice = select_option("Choose a post-harvest tool to run:", [
            "DNS & Subdomain Enumeration",
            "Nmap",
            "Searchsploit",
            "Shodan",
            "View Results",
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
        elif choice == "Exit":
            break

def main():
    check_environment()
    session = SessionManager()
    session.init_session()

    run_theharvester(session)
    review_results(session)
    tools_menu(session)

if __name__ == "__main__":
    main()
