# report_exporter.py

import os
from datetime import datetime
from rich.console import Console
from rich.prompt import Prompt
import questionary

console = Console()

def export_session_report(session_manager):
    session_data = session_manager.session_data
    pool = session_data["result_pool"]
    tool_runs = session_data["tools_run"]

    result_keys = list(pool.keys())
    selected = questionary.checkbox(
        "Select which results to include in the report:",
        choices=result_keys
    ).ask()

    if not selected:
        console.print("[italic]No result types selected.[/italic]")
        return

    format_choice = questionary.select(
        "Choose report format:",
        choices=["Markdown (.md)", "Plain text (.txt)"]
    ).ask()

    is_md = format_choice.startswith("Markdown")

    output_dir = session_manager.session_path
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    ext = "md" if is_md else "txt"
    filename = f"report_{timestamp}.{ext}"
    filepath = os.path.join(output_dir, filename)

    lines = []

    if is_md:
        lines.append(f"# OSINT Session Report\n\n")
    else:
        lines.append("OSINT Session Report\n====================\n")

    lines.append(f"Session: {session_manager.session_name}")
    lines.append(f"Generated: {timestamp}\n")

    for key in selected:
        values = pool.get(key, [])
        if not values:
            continue

        section_title = key.replace("_", " ").title()
        if is_md:
            lines.append(f"\n## {section_title}")
        else:
            lines.append(f"\n{section_title}\n{'-' * len(section_title)}")

        if isinstance(values[0], dict):
            for item in values:
                for k, v in item.items():
                    lines.append(f"- {k.title()}: {v}")
                lines.append("")  # space between entries
        else:
            for val in values:
                lines.append(f"- {val}")
        lines.append("")

    with open(filepath, "w") as f:
        f.write("\n".join(lines))

    console.print(f"[green]Report saved to:[/green] {filepath}")
