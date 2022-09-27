from crc_cli import memo

from crc_calculation import utils
from crc_calculation import crc_calculator
from cli.menus import crc_standard_menu
import cli.input_handlers.raw_input_handler as r_inp


def crc_program():
    print("==== Message M(x) ====")
    msg, msg_len = r_inp.get_bin_str_inp()
    if msg is None:
        print("Aborted.\n")
        return
    print()
    print("==== Divisor P(x) ====")
    divisor = crc_standard_menu.choose_crc_standard()
    if divisor is None:
        return

    memo.store_codeword(
        crc_calculator.get_codeword(msg, msg_len, divisor, memo.divisor_msb)
    )
    print(f"Codeword: {memo.codeword:0{utils.get_bin_length(memo.codeword)}b}")
    print()
