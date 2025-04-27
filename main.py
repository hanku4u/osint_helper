# main.py

from startup import environment_check
from app.cli import main_menu

if __name__ == "__main__":
    environment_check()
    main_menu()
