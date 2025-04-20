# session_manager.py

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
                "usernames": []
            }
        }

    def init_session(self):
        # Ask for session name
        self.session_name = Prompt.ask("Enter a session name", default=datetime.now().strftime("session-%Y%m%d-%H%M%S"))

        # Ask for (or confirm) output directory
        self.output_dir = Prompt.ask("Enter output directory", default=DEFAULT_OUTPUT_DIR)

        # Full path for this session
        self.session_path = os.path.join(self.output_dir, self.session_name)

        # Create directory if it doesn't exist
        os.makedirs(self.session_path, exist_ok=True)

        # Path to session.json
        self.session_file = os.path.join(self.session_path, "session.json")

        # Load session if already exists
        if os.path.exists(self.session_file):
            console.print("[yellow]Loading existing session file.[/yellow]")
            with open(self.session_file, "r") as f:
                self.session_data = json.load(f)
        else:
            self.save_session()

        console.print(f"[green]Session initialized at:[/green] {self.session_path}")

    def save_session(self):
        with open(self.session_file, "w") as f:
            json.dump(self.session_data, f, indent=4)

    def get_output_path_for_tool(self, tool_name):
        tool_dir = os.path.join(self.session_path, tool_name)
        os.makedirs(tool_dir, exist_ok=True)
        return tool_dir

    def add_tool_run(self, tool_name, input_value, output_file=None, parsed_file=None):
        self.session_data["tools_run"].append({
            "tool": tool_name,
            "input": input_value,
            "output_file": output_file,
            "parsed_file": parsed_file,
            "timestamp": datetime.now().isoformat()
        })
        self.save_session()

    def update_result_pool(self, key, values):
        if key in self.session_data["result_pool"]:
            self.session_data["result_pool"][key].extend(v for v in values if v not in self.session_data["result_pool"][key])
            self.save_session()

    def get_result_pool(self):
        return self.session_data["result_pool"]
