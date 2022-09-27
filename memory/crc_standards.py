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
