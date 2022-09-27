from crc_cli import memo

from crc_calculation import utils
from crc_calculation import crc_calculator
from cli.menus import message_menu
from cli.menus import crc_standard_menu


def crc_program():
    message = message_menu.get_message()
    if message is None:
        return
    print()
    print("==== Divisor P(x) ====")
    divisor = crc_standard_menu.choose_crc_standard()
    if divisor is None:
        return

    crc_calculator.get_codeword(message[0], message[1], divisor, memo.divisor_msb)

    print(f"Codeword: {memo.codeword:0{utils.get_bin_length(memo.codeword)}b}")
    print()
