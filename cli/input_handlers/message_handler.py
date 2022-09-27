import cli.input_handlers.raw_input_handler as r_inp
from crc_cli import memo


def message_handler():
    while 1:
        inp = r_inp.get_user_input()
        if memo.has_codeword_memory and memo.has_crc_memory and inp == "0":
            return (
                memo.codeword << memo.divisor_msb,
                memo.codeword_len - memo.divisor_msb,
            )
        elif inp == "1":
            user_cw_bin_str, len = r_inp.get_bin_str_inp()
            if user_cw_bin_str is None:
                return None
            return user_cw_bin_str, len
        elif inp == "q":
            return None
        else:
            print("Invalid input")
