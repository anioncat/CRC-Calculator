from cli.input_handlers import user_crc_handler


def user_crc_routine() -> int:
    """Handles user defined CRC code

    Returns:
        int: 0 on completion, None on quit
    """
    num_bits = user_crc_handler.get_div_bits()
    if num_bits is None:
        # Aborted.
        return lambda: print("Aborted.\n")
    return user_crc_handler.get_divsor(num_bits)
