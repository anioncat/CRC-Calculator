from cli.input_handlers import message_handler

from crc_cli import memo


def get_message():
    print("==== Message M(x) ====")
    if memo.has_codeword_memory and memo.has_crc_memory:
        print(f"0 - Last produced message {memo.codeword>>memo.divisor_msb:0b}")
    print("1 - Enter a new message")
    print("q - Return to Main Menu")
    print()
    return message_handler.message_handler()
