# main.py

from startup import environment_check
from textual.app import App, ComposeResult
from textual.widgets import Static, Button
from app.ui.menu import MainMenu 
from app.tools.harvester_runner import run_theharvester

class OSINTApp(App):
    """Main application for the OSINT CLI Toolkit."""

    CSS_PATH = None  # We'll add styling later

    def compose(self) -> ComposeResult:
        yield MainMenu()

    async def run_theharvester_flow(self):
        """Prompt for domain and custom args, then run theHarvester."""
        self.console.log("[*] Starting theHarvester scan...")

        domain = await self.prompt("Enter the domain or IP to scan with theHarvester:")
        if not domain:
            self.console.log("[!] No domain entered. Returning to menu.")
            return

        custom_args = await self.prompt("Enter any custom theHarvester arguments (or leave blank):")

        self.console.log(f"[*] Running theHarvester on {domain}...")
        output_path = run_theharvester(domain, custom_args)

        if output_path:
            self.console.log(f"[+] theHarvester output saved to {output_path}")
        else:
            self.console.log("[!] theHarvester scan failed.")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "exit":
            self.exit()
        elif button_id == "harvester":
            await self.run_theharvester_flow()
        else:
            self.console.log(f"You selected: {button_id} (Feature coming soon!)")

if __name__ == "__main__":
    environment_check()  # Check environment before running app
    OSINTApp().run()
