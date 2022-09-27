import cli.input_handlers.raw_input_handler as r_inp

from crc_cli import memo


def get_div_bits():
    print(
        "\nEnter the number of bits in the divisor (h for help, q to return to selection):"
    )
    num_bits = -1
    while num_bits < 0:
        usr_msb = r_inp.get_user_input()
        if usr_msb == "h":
            print("The number of bits is equal to the most significant bit + 1")
            print(
                "Given x^2 + x + 1, the most significant bit, "
                "n is 2, the number of bits is 3\n"
            )
            continue  # do not update num_bits
        if usr_msb == "q":
            return None
        try:
            num_bits = int(usr_msb)
        except ValueError:
            print("\nFailed to convert to number")
            continue
        if num_bits <= 1:
            print("\nThere must be more than 2 or more bits in the divisor")
            num_bits = -1
    print()
    return num_bits


def get_divsor(num_bits: int):
    print("==== Divisor P(x) ====")
    print(f"Divisor of length {num_bits} was specified\n")
    valid = False
    while not valid:
        inp_bin_str, bin_str_len = r_inp.get_bin_str_inp()
        if inp_bin_str is None:
            return lambda: print("Aborted.\n")
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
    return memo.divisor
