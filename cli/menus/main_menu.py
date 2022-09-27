from cli.input_handlers import main_menu_handler


def menu():
    """The main menu. Only q or ^c will exit."""
    while 1:
        print(
            """==== MAIN MENU ====
Please enter the menu item number followed by enter (e.g. h).

1 - CRC calculation
2 - CRC validation
3 - Credits
h - Information
q - Quit
"""
        )
        menu_result = main_menu_handler.menu_inp_handler()
        menu_result()


def cli_main():
    print()
    print("Welcome to a CRC simulator in Python")
    print("------------------------------------")
    print()
    menu()
