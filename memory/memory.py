from memory.crc_standards import CrcStandards


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
