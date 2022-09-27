# -- coding: utf-8 --

from memory.memory import Memory
from cli.menus import main_menu

# Global memory of the application
memo = Memory()


def main():
    main_menu.cli_main()


if __name__ == "__main__":
    main()
