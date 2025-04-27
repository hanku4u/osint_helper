# main.py

from startup import environment_check
from textual.app import App, ComposeResult
from textual.widgets import Button, Static
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

        def get_inputs():
            domain = input("Enter the domain or IP to scan with theHarvester: ")
            custom_args = input("Enter any custom theHarvester arguments (or leave blank): ")
            return domain, custom_args

        domain, custom_args = await self.run_worker(get_inputs)

        if not domain:
            self.console.log("[!] No domain entered. Returning to menu.")
            return

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
