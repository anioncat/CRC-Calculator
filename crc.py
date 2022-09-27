# -- coding: utf-8 --

import sys

if sys.platform.startswith("win"):
    import os

    os.system("color")


class TextColours:
    crc = "\x1b[43m\x1b[30m"
    dragged_bit = "\x1b[36m"
    success = "\x1b[92m"
    fail = "\x1b[91m"
    reset = "\x1b[0m"


class CrcStandards:
    # Index
    NAME = 0
    DIVISOR = 1
    MSB = 2
    DESCRIPTION = 3

    crc_standards = [
        (
            "CRC-16",
            0x8005,
            16,
            "Most commonly used checksum, such as in USB. Also known as CRC-16-ANSI",
        ),
        ("CRC-16-CCITT", 0x1021, 16, "Used in applications such as Bluetooth"),
        ("CRC-12", 0x80F, 12, "Used in telecomm systems"),
        ("CRC-32", 0x04C11DB7, 32, "Used in applications such as SATA"),
        ("CRC-8", 0xD5, 8, "Used is digital video broadcasting"),
        ("CRC-1 (Parity bit)", 0x1, 1, "Also known as the parity bit"),
    ]

    def get_name(index: int):
        return CrcStandards.crc_standards[index][CrcStandards.NAME]

    def get_div(index: int):
        return CrcStandards.crc_standards[index][CrcStandards.DIVISOR]

    def get_msb(index: int):
        return CrcStandards.crc_standards[index][CrcStandards.MSB]

    def get_desc(index: int):
        return CrcStandards.crc_standards[index][CrcStandards.DESCRIPTION]


class Memory:
    has_codeword_memory: bool = False
    codeword: int = 0

    has_crc_memory: bool = False
    divisor: int = 0
    divisor_name: str = ""
    divisor_msb: int = 0

    def store_divisor(self, index: int):
        if index == -1:
            # Return early, nothing needs to change
            return
        self.divisor_name = CrcStandards.get_name(index)
        self.divisor = CrcStandards.get_div(index)
        self.divisor_msb = CrcStandards.get_msb(index)
        self.has_crc_memory = True

    def store_codeword(self, codeword: int):
        self.has_codeword_memory = True
        self.codeword = codeword

    def create_poly_str(self) -> str:
        """Converts the divisor in memory into polynomial form

        Returns:
            str: list of polynomials
        """
        poly_list = list()
        for i, binary in enumerate(f"{self.divisor:0b}"):
            if binary == "1":
                poly_list.append(f"x^{self.divisor_msb - i}")
        return "".join(["1" if i == "x^0" else f"{i} + " for i in poly_list])


# Global memory of the application
memo = Memory()


### Input handling ###


def get_user_input() -> str:
    print("> ", end="")
    return input()


def get_bin_str_inp() -> tuple:
    print("Enter binary string (1 and 0 only, q to return):")
    user_input = get_user_input()
    valid = False
    while not valid:
        if user_input == "q":
            return None, -1
        valid = True
        for c in user_input:
            # Check for bin string
            if c != "0" and c != "1":
                print(f"Character {c} detected. Wrong format.")
                valid = False
                break
        if not valid:
            print("Enter binary string (1 and 0 only):")
            user_input = get_user_input()
    input_len = len(user_input)
    # Convert to integer (use bin manip)
    return int("0b" + user_input, 2), input_len


def get_bin_length(val: int) -> int:
    # bin(val) gives "0bxxxx", get rid of the 0b
    return len(bin(val)) - 2
    # return val.bit_length()  # this is apparently slower


### Calculation ###


class CrcCalcPrinter:
    """
    Printing is performed in class to maintain its own variables and keep
    the calculation clean
    """

    verbose: bool = False  # If not verbose no need to print anything
    tot_len: int
    div_str: str
    div_len: int
    code_str: str
    code_len: int
    from_start: int
    step_from_start: int
    from_end: int

    def __init__(
        self,
        verbose: bool,
        total_len: int,
        codeword: int,
        codeword_len: int,
        divisor: int,
        divisor_len: int,
    ):
        if verbose and total_len > 0:
            self.verbose = verbose
            self.tot_len = total_len
            self.code_str = bin(codeword)[2:]
            self.code_len = codeword_len
            self.div_str = bin(divisor)[2:]
            self.div_len = divisor_len
            self.from_start = total_len - codeword_len
            self.from_end = total_len - divisor_len
            print("Calculating CRC code:")
            print(f"{codeword:0{total_len}b}")

    def colour_dragged_bits(self, dragged_bits: str):
        return f"{TextColours.dragged_bit}{dragged_bits}{TextColours.reset}"

    def print_step(self, xor_result: int, new_code_len: int):
        if not self.verbose:
            return
        # Print divisor and divisor line
        print(
            f"{' ' * self.from_start}{self.div_str}{' ' * (self.from_end - self.from_start)} XOR"
        )
        print(f"{' ' * self.from_start}{'-' * self.div_len}")
        # Store prev from start
        self.step_from_start = self.from_start
        # Update code lengths
        self.code_len = new_code_len
        self.from_start = self.tot_len - self.code_len
        trailing_add = self.code_str[
            self.div_len + self.step_from_start : self.div_len + self.from_start
        ]
        # Print result
        if self.code_len < self.div_len:
            fancy_crc_end = f"{xor_result:0{self.div_len}b}{trailing_add}"
            fce_len = len(fancy_crc_end)
            fancy_crc_end = (
                fancy_crc_end[0 : fce_len - memo.divisor_msb]
                + TextColours.crc
                + fancy_crc_end[fce_len - memo.divisor_msb :]
                + TextColours.reset
            )
            print(f"{' ' * self.step_from_start}{fancy_crc_end} Done")
        else:
            print(
                f"{' ' * self.step_from_start}{xor_result:0{self.div_len}b}{self.colour_dragged_bits(trailing_add)}"
            )


def calc_crc(
    codeword: int, divisor: int, total_len: int = -1, verbose: bool = True
) -> int:
    """Calculates the CRC based on the codeword and divisor"""
    # Get the lengths need for calculation, ignoring lead 0s
    divisor_len = get_bin_length(divisor)
    codeword_len = get_bin_length(codeword)
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
        codeword_len = get_bin_length(codeword)
        crc_step_printer.print_step(xor_result, codeword_len)
    return codeword


def get_crc_code(msg: int, msg_len: int, divisor: int, verbose: bool = True) -> int:
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
    crc_len = get_bin_length(divisor) - 1
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
    crc = get_crc_code(msg, msg_len, divisor, verbose=verbose)
    print()
    print(f"CRC Code: {' ' * msg_len}{crc:0{divisor_len}b}")
    # Append CRC to message
    code_word = msg << divisor_len | crc
    return code_word


### Codeword calculation ###


def crc_help() -> int:
    print("==== INFORMATION ====")
    if memo.has_crc_memory:
        print(f"0 - Last used CRC was {memo.divisor_name}")
    for i in range(len(CrcStandards.crc_standards)):
        print(f"{i} - {CrcStandards.get_name(i)}. {CrcStandards.get_desc(i)}")
    print()
    return -1


def user_crc_routine() -> int:
    """Handles user defined CRC code

    Returns:
        int: 0 on completion, -1 on quit
    """
    print(
        "\nEnter the number of bits in the divisor (h for help, q to return to selection):"
    )
    num_bits = -1
    while num_bits < 0:
        usr_msb = get_user_input()
        if usr_msb == "h":
            print("The number of bits is equal to the most significant bit + 1")
            print(
                "Given x^2 + x + 1, the most significant bit, "
                "n is 2, the number of bits is 3\n"
            )
            continue  # do not update num_bits
        if usr_msb == "q":
            print("Aborted.\n")
            return -1
        try:
            num_bits = int(usr_msb)
        except ValueError:
            print("\nFailed to convert to number")
            continue
        if num_bits <= 1:
            print("\nThere must be more than 2 or more bits in the divisor")
            num_bits = -1
    print()
    print("==== Divisor P(x) ====")
    print(f"Divisor of length {num_bits} was specified\n")
    valid = False
    while not valid:
        inp_bin_str, bin_str_len = get_bin_str_inp()
        if inp_bin_str is None:
            print("Aborted.\n")
            return -1
        valid = True
        if bin_str_len > num_bits:
            print("\nMore bits found than specified")
            valid = False
        if inp_bin_str % 2 == 0:
            print("\nFinal bit should be 1")
            valid = False
    # Store when valid
    memo.divisor = inp_bin_str
    if bin_str_len < num_bits:
        print("Most significant bit will be appended")
    elif f"{memo.divisor:0{bin_str_len}b}"[0] == "0":
        print("Leading 0 will be replaced with 1")
    print()
    memo.divisor_name = "User defined"
    memo.divisor_msb = num_bits - 1
    memo.has_crc_memory = True
    return 0


def crc_div_inp_handler() -> int:
    # Map crc standards to inputs
    divisor_mapping = dict()
    for i in range(len(CrcStandards.crc_standards)):
        divisor_mapping[f"{i+1}"] = CrcStandards.get_div(i)
    # Last used crc
    if memo.has_crc_memory:
        divisor_mapping["0"] = memo.divisor

    inp = get_user_input()
    if len(inp) == 0:
        inp = "0"
    if inp == f"{len(CrcStandards.crc_standards) + 1}":
        return user_crc_routine
    elif inp == "h":
        return crc_help
    elif inp == "q":
        return None
    elif inp not in divisor_mapping.keys():
        return lambda: print("Invalid input.")
    else:
        memo.store_divisor(int(inp) - 1)
        return divisor_mapping[inp]


def choose_crc_standard() -> int:
    crc_inp_return = -1
    while crc_inp_return < 0:
        print("Please choose a CRC divisor:")
        if memo.has_crc_memory:
            print(f"0 - Last used {memo.divisor_name}")
        for i in range(len(CrcStandards.crc_standards)):
            print(f"{i+1} - {CrcStandards.get_name(i)}")
        print(f"{len(CrcStandards.crc_standards)+1} - Enter your own divisor")
        print("h - Information")
        print("q - Return to Main Menu")
        print()

        crc_inp_return = crc_div_inp_handler()
        if not isinstance(crc_inp_return, int):
            if crc_inp_return is None:
                return None
            # Then is a function
            crc_inp_return = crc_inp_return()
            crc_inp_return = -1
    # Add most significant bit
    memo.divisor = memo.divisor | (1 << memo.divisor_msb)
    print(f"Divisor:    {memo.divisor_name}")
    print(f"Binary:     {memo.divisor:0b}")
    print(f"Polynomial: {memo.create_poly_str()}")
    print()
    return memo.divisor


def crc_program():
    print("==== Message M(x) ====")
    msg, msg_len = get_bin_str_inp()
    if msg is None:
        print("Aborted.\n")
        return
    print()
    print("==== Divisor P(x) ====")
    divisor = choose_crc_standard()
    if divisor is None:
        return

    memo.store_codeword(get_codeword(msg, msg_len, divisor, memo.divisor_msb))
    print(f"Codeword: {memo.codeword:0{get_bin_length(memo.codeword)}b}")
    print()


### CRC Validation ###


def check_codeword(codeword: int, divisor: int, verbose: bool = True):
    print("Checking code word...")
    crc_chk = calc_crc(codeword, divisor, get_bin_length(codeword), verbose=verbose)
    if crc_chk == 0:
        msg = f"{TextColours.success}Success{TextColours.reset}"
        memo.store_codeword(codeword)
    else:
        msg = f"{TextColours.fail}Fail{TextColours.reset}"
    print()
    print(f"Check result: {crc_chk:0{memo.divisor_msb}b}, [[{msg}]]")
    print()


def val_codeword_handler():
    while 1:
        inp = get_user_input()
        if memo.has_codeword_memory and inp == "0":
            return memo.codeword
        elif inp == "1":
            user_cw_bin_str = get_bin_str_inp()[0]
            if user_cw_bin_str is None:
                return None
            memo.store_codeword(user_cw_bin_str)
            return user_cw_bin_str
        elif inp == "q":
            return None
        else:
            print("Invalid input")


def get_val_codeword():
    print("==== Codeword ====")
    if memo.has_codeword_memory:
        print(f"0 - Last produced codeword {memo.codeword:0b}")
    print("1 - Enter your own codeword")
    print("q - Return to Main Menu")
    print()
    return val_codeword_handler()


def crc_validation():
    codeword = get_val_codeword()
    if codeword is None:
        print()
        return
    print()
    crc = choose_crc_standard()
    if crc is None:
        return
    check_codeword(codeword, crc)


### Main menu ###


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


def quit_program():
    print("Quitting.\n")
    quit(0)


def print_help():
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


def menu_inp_handler():
    """
    Handler for the main menu.
    Returns a callable corresponding to the menu item
    """
    menu_func_mapping = {
        "1": crc_program,
        "2": crc_validation,
        "c": print_credits,  # C for credits.
        "3": print_credits,
        "4": print_help,  # Since its in order 4 makes sense to accidentally press
        "h": print_help,
        "q": quit_program,
    }
    inp = get_user_input()

    if inp not in menu_func_mapping.keys():
        return lambda: print("Invalid input.\n")
    else:
        return menu_func_mapping[inp]


def menu():
    """The main menu. Only q or ^c will exit."""
    while 1:
        print(
            """==== MAIN MENU ====
Please enter the menu item number followed by enter (e.g. h).

1 - CRC conversion
2 - CRC validation
3 - Credits
h - Information
q - Quit
"""
        )
        menu_result = menu_inp_handler()
        menu_result()


def main():
    print()
    print("Welcome to a CRC simulator in Python")
    print("------------------------------------")
    print()
    menu()


if __name__ == "__main__":
    main()
