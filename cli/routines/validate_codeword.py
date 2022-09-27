from cli.menus import validate_crc_menu, crc_standard_menu
from crc_calculation import crc_calculator


def crc_validation():
    codeword = validate_crc_menu.get_val_codeword()
    if codeword is None:
        print()
        return
    print()
    crc = crc_standard_menu.choose_crc_standard()
    if crc is None:
        return
    crc_calculator.check_codeword(codeword, crc)
