from cli.input_handlers import codeword_handler

from crc_cli import memo


def get_codeword():
    print("==== Codeword ====")
    if memo.has_codeword_memory:
        print(f"0 - Last produced codeword {memo.codeword:0b}")
    print("1 - Enter your own codeword")
    print("q - Return to Main Menu")
    print()
    return codeword_handler.codeword_handler()
