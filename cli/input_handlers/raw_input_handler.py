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
