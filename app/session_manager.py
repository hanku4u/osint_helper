import os
import json
from datetime import datetime
from rich.prompt import Prompt
from rich.console import Console

console = Console()

DEFAULT_OUTPUT_DIR = "./results"

class SessionManager:
    def __init__(self):
        self.output_dir = DEFAULT_OUTPUT_DIR
        self.session_name = None
        self.session_path = None
        self.session_data = {
            "tools_run": [],
            "result_pool": {
                "emails": [],
                "domains": [],
                "subdomains": [],
                "ips": [],
                "usernames": [],
                "nmap_services": []
            }
        }

    def init_session(self):
        self.session_name = Prompt.ask(
            "Enter a session name",
            default=datetime.now().strftime("session-%Y%m%d-%H%M%S")
        )

        self.output_dir = Prompt.ask(
            "Enter output directory",
            default=DEFAULT_OUTPUT_DIR
        )
