import cli.input_handlers.raw_input_handler as r_inp
import cli.routines.user_crc_divisor
from crc_calculation import utils
from memory.memory import CrcStandards

from crc_cli import memo


def crc_div_menu_handler() -> int:
    # Map crc standards to inputs
    divisor_mapping = dict()
    for i in range(len(CrcStandards.crc_standards)):
        divisor_mapping[f"{i+1}"] = CrcStandards.get_div(i)
    # Last used crc
    if memo.has_crc_memory:
        divisor_mapping["0"] = memo.divisor

    inp = r_inp.get_user_input()
    if len(inp) == 0:
        inp = "0"
    if inp == f"{len(CrcStandards.crc_standards) + 1}":
        return cli.routines.user_crc_divisor.user_crc_routine()
    elif inp == "h":
        return utils.crc_help
    elif inp == "q":
        return None
    elif inp not in divisor_mapping.keys():
        return lambda: print("Invalid input.")
    else:
        memo.store_divisor(int(inp) - 1)
        return divisor_mapping[inp]
