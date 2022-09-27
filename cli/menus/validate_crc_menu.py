from cli.input_handlers import validate_codeword_handler

from crc_cli import memo


def get_val_codeword():
    print("==== Codeword ====")
    if memo.has_codeword_memory:
        print(f"0 - Last produced codeword {memo.codeword:0b}")
    print("1 - Enter your own codeword")
    print("q - Return to Main Menu")
    print()
    return validate_codeword_handler.val_codeword_handler()
