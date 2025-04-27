import sys
import subprocess
import importlib.util
import os

REQUIRED_PYTHON = (3, 11)
REQUIRED_PACKAGES = ["textual", "rich"]

def check_python_version():
    if sys.version_info < REQUIRED_PYTHON:
        print(f"[!] Python {REQUIRED_PYTHON[0]}.{REQUIRED_PYTHON[1]} or higher is required.")
        print(f"[!] You are running Python {sys.version_info.major}.{sys.version_info.minor}.")
        sys.exit(1)

def check_missing_packages():
    missing = []
    for package in REQUIRED_PACKAGES:
        if importlib.util.find_spec(package) is None:
            missing.append(package)
    return missing

def install_packages(packages):
    try:
        subprocess.check_call(["pip", "install", *packages])
    except subprocess.CalledProcessError:
        print("[!] Failed to install required packages.")
        sys.exit(1)

def check_sqlite3_support():
    try:
        import sqlite3
        # Try a basic in-memory connection
        conn = sqlite3.connect(":memory:")
        conn.close()
    except Exception as e:
        print("[!] Your Python installation does not support SQLite3.")
        print(f"[!] Error: {e}")
        sys.exit(1)

def environment_check():
    check_python_version()
    check_sqlite3_support()
    missing = check_missing_packages()

    if missing:
        print(f"[!] Missing required packages: {', '.join(missing)}")
        choice = input("[?] Would you like to install them now? (y/n): ").strip().lower()
        if choice == 'y':
            install_packages(missing)
            print("[+] Dependencies installed successfully. Restarting script...")
            os.execv(sys.executable, [sys.executable] + sys.argv)
        else:
            print("[!] Exiting. Please install the required packages manually.")
            sys.exit(1)

if __name__ == "__main__":
    environment_check()
