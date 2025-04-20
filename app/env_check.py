# env_check.py

import sys
import subprocess
import importlib.util
import shutil

MIN_PYTHON = (3, 11)
REQUIRED_PACKAGES = ["rich"]

def check_python_version():
    if sys.version_info < MIN_PYTHON:
        sys.exit(f"[ERROR] Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]} or higher is required.\nYou have Python {sys.version_info.major}.{sys.version_info.minor}")

def is_package_installed(package_name):
    return importlib.util.find_spec(package_name) is not None

def install_missing_packages(missing):
    uv_path = shutil.which("uv")
    if not uv_path:
        sys.exit("[ERROR] 'uv' is not installed or not in your PATH. Please install it manually first.")

    print(f"\n[INFO] Missing required packages: {', '.join(missing)}")
    confirm = input("Would you like to install them automatically using uv? (y/N): ").strip().lower()
    if confirm == "y":
        try:
            subprocess.run(["uv", "pip", "install", *missing], check=True)
        except subprocess.CalledProcessError:
            sys.exit("[ERROR] Failed to install required packages with uv.")
    else:
        sys.exit("[INFO] Exiting so you can install them manually.")

def check_environment():
    check_python_version()
    missing = [pkg for pkg in REQUIRED_PACKAGES if not is_package_installed(pkg)]
    if missing:
        install_missing_packages(missing)
