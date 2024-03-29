import cli.input_handlers.raw_input_handler as r_inp
from crc_cli import memo


def codeword_handler():
    while 1:
        inp = r_inp.get_user_input()
        if memo.has_codeword_memory and inp == "0":
            return memo.codeword
        elif inp == "1":
            user_cw_bin_str, len = r_inp.get_bin_str_inp()
            if user_cw_bin_str is None:
                return None
            memo.store_codeword(user_cw_bin_str, len)
            return user_cw_bin_str
        elif inp == "q":
            return None
        else:
            print("Invalid input")
