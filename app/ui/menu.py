# app/ui/menu.py

from textual.widgets import Static, Button
from textual.containers import Vertical
from textual.app import ComposeResult

class MainMenu(Static):
    """Main menu widget with navigation buttons."""

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Button("Run theHarvester", id="harvester")
            yield Button("Run DNS Enumeration", id="dns")
            yield Button("Run WHOIS Lookup", id="whois")
            yield Button("Run Nmap Scan", id="nmap")
            yield Button("Review Current Session Data", id="review")
            yield Button("Export Report", id="export")
            yield Button("Exit", id="exit")
