from memory.crc_standards import CrcStandards

from crc_cli import memo


class TextColours:
    crc = "\x1b[43m\x1b[30m"
    dragged_bit = "\x1b[36m"
    success = "\x1b[92m"
    fail = "\x1b[91m"
    reset = "\x1b[0m"

    def colour_dragged_bits(dragged_bits: str):
        return f"{TextColours.dragged_bit}{dragged_bits}{TextColours.reset}"

    def colour_val_result(success: bool):
        if success:
            return f"{TextColours.success}Success{TextColours.reset}"
        else:
            return f"{TextColours.fail}Fail{TextColours.reset}"


def get_bin_length(val: int) -> int:
    # bin(val) gives "0bxxxx", get rid of the 0b
    return len(bin(val)) - 2
    # return val.bit_length()  # this is apparently slower


def print_credits():
    print(
        """
+-------------------+
| CRC Simulator by: |
|     Anakin Bawden |
|     Ethan Wang    |
|     Sean Randell  |
|                   |
| RMIT DCNC 2022    |
+-------------------+
"""
    )


def crc_help() -> int:
    print("==== INFORMATION ====")
    if memo.has_crc_memory:
        print(f"0 - Last used CRC was {memo.divisor_name}")
    for i in range(len(CrcStandards.crc_standards)):
        print(f"{i+1} - {CrcStandards.get_name(i)}. {CrcStandards.get_desc(i)}")
    print()
    return -1


def print_main_menu_help():
    print(
        """
==== INFORMATION ====
1   - Create a CRC codeword which would be sent over a network.
      Enter a message then choose a CRC polynomial, the program will return
        a codeword.
        
2   - Validate a CRC codeword which would be received over the network.
      Provide a codeword (with the CRC) then choose the CRC polynomial to
        validate the codeword.
        
Terms
-----
CRC        - Cyclic Redundancy Check
             CRC will continuously xor a codeword on its most significant bit
               until there is not enough bits to divide in which it will carry
               the 0's and stop. The result will be appended to the end of the
               message which can be reversed on the other end to validate the
               code word.

Codeword   - The message after the message is appended with the CRC bits

Polynomial - CRC polynomials map to binary by the presence of terms x^i in the
               polynomial where the the leading term of the polynomial is x^n,
               n >= 0 and n >= i >= 0.
             So, x^2 + 1 maps to the binary 101 (since 1 = x^0).
"""
    )


def quit_program():
    print("Quitting.\n")
    quit(0)
