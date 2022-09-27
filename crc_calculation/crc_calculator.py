import crc_calculation.utils as utils
from crc_calculation.calculator_print_helper import CrcCalcPrinter

from crc_cli import memo


def calc_crc(
    codeword: int, divisor: int, total_len: int = -1, verbose: bool = True
) -> int:
    """Calculates the CRC based on the codeword and divisor"""
    # Get the lengths need for calculation, ignoring lead 0s
    divisor_len = utils.get_bin_length(divisor)
    codeword_len = utils.get_bin_length(codeword)
    # Initialise the printer
    crc_step_printer = CrcCalcPrinter(
        verbose, total_len, codeword, codeword_len, divisor, divisor_len
    )
    while codeword_len >= divisor_len:
        # Get the value to xor
        len_diff = codeword_len - divisor_len
        bin_to_xor = codeword >> len_diff
        # Perform division
        xor_result = bin_to_xor ^ divisor
        # Update message with result
        mask = (1 << len_diff) - 1  # For copying down the codeword after the result
        codeword = (codeword & mask) | (xor_result << len_diff)  # Combine results
        # Next iteration
        codeword_len = utils.get_bin_length(codeword)
        crc_step_printer.print_step(xor_result, codeword_len)
    return codeword


def _get_crc_code(msg: int, msg_len: int, divisor: int, verbose: bool = True) -> int:
    """Convert the message into a codeword, appending 0's need for the CRC.
    Then calculates the CRC and returns the codeword

    Args:
        msg (int): The message to validate.
        msg_len (int): The length of the message (including leading 0s).
        divisor (int): The divisor for checking.
        verbose (bool, optional): Whether to print steps. Defaults to True.

    Returns:
        int: The codeword
    """
    crc_len = utils.get_bin_length(divisor) - 1
    # Bitshift divisor len - 1
    code = msg << crc_len
    if verbose:
        print(f"Appending {crc_len} zeros")
    return calc_crc(code, divisor, msg_len + crc_len, verbose=verbose)


def get_codeword(
    msg: int, msg_len: int, divisor: int, divisor_len: int, verbose: bool = True
) -> int:
    """Takes a message and returns the codeword with CRC

    Args:
        msg (int): The message
        msg_len (int): The length of the message
        divisor (int): The divisor
        divisor_len (int): The length of the divisor
        verbose (bool, optional): Whether to print steps. Defaults to True.

    Returns:
        int: The message with CRC check appened
    """
    crc = _get_crc_code(msg, msg_len, divisor, verbose=verbose)
    print()
    print(f"CRC Code: {' ' * msg_len}{crc:0{divisor_len}b}")
    # Append CRC to message
    code_word = msg << divisor_len | crc
    return code_word


def check_codeword(codeword: int, divisor: int, verbose: bool = True):
    print("Checking code word...")
    crc_chk = calc_crc(
        codeword, divisor, utils.get_bin_length(codeword), verbose=verbose
    )
    if crc_chk == 0:
        memo.store_codeword(codeword)
    print()
    print(
        f"Check result: {crc_chk:0{memo.divisor_msb}b}, [[{utils.TextColours.colour_val_result(crc_chk == 0)}]]"
    )
    print()
