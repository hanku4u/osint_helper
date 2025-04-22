from textual.widget import Widget
from app.utils.db import initialize_db, fetch_data

class SessionReview(Widget):
    def on_mount(self):
        initialize_db()
        emails = fetch_data("emails")
        if not emails:
            self.update("No data available in the session.")
        else:
            formatted_emails = "\n".join(emails)
            self.update(f"Fetched Emails:\n{formatted_emails}")