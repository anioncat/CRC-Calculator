from crc_cli import memo
from memory.crc_standards import CrcStandards
from cli.input_handlers import crc_choice_handler


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

        crc_inp_return = crc_choice_handler.crc_div_menu_handler()

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
