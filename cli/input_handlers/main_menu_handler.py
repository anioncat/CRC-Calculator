from crc_calculation import utils
import cli.input_handlers.raw_input_handler as r_inp

import cli.routines.create_codeword
import cli.routines.validate_codeword


def menu_inp_handler():
    """
    Handler for the main menu.
    Returns a callable corresponding to the menu item
    """
    menu_func_mapping = {
        "1": cli.routines.create_codeword.crc_program,
        "2": cli.routines.validate_codeword.crc_validation,
        "c": utils.print_credits,  # C for credits.
        "3": utils.print_credits,
        "4": utils.print_main_menu_help,  # Since its in order 4 makes sense to accidentally press
        "h": utils.print_main_menu_help,
        "q": utils.quit_program,
    }
    inp = r_inp.get_user_input()

    if inp not in menu_func_mapping.keys():
        return lambda: print("Invalid input.\n")
    else:
        return menu_func_mapping[inp]
