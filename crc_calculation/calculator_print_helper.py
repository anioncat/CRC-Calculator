import sys

from crc_calculation.utils import TextColours

from crc_cli import memo

if sys.platform.startswith("win"):
    import os

    os.system("color")


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
                f"{' ' * self.step_from_start}{xor_result:0{self.div_len}b}{TextColours.colour_dragged_bits(trailing_add)}"
            )
