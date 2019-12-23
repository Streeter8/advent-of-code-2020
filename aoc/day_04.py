START = 178416
END = 676461


class Code:
    def __init__(self, code: int):
        self.code = code
        self.str_code = str(code)

    @property
    def is_valid_code(self) -> bool:
        return (
            self.is_six_digit_number
            and self.within_initial_range
            and self.has_two_adjacent_equal_numbers
            and self.is_increasing_number
        )

    @property
    def is_six_digit_number(self) -> bool:
        return len(self.str_code) == 6

    @property
    def within_initial_range(self) -> bool:
        return START <= self.code <= END

    @property
    def has_two_adjacent_equal_numbers(self) -> bool:
        for index in range(len(self.str_code) - 1):
            if self.str_code[index] == self.str_code[index + 1]:
                return True
        return False

    @property
    def is_increasing_number(self) -> bool:
        for index in range(len(self.str_code) - 1):
            if int(self.str_code[index]) > int(self.str_code[index + 1]):
                return False
        return True

    @property
    def largest_multiple_digit(self) -> bool:
        for index in range(len(self.str_code) - 1):
            if int(self.str_code[index]) > int(self.str_code[index + 1]):
                return False
        return True


class AocFour:
    def range_part_one(self):
        total = self.get_total_valid_inputs(START, END)
        print(f"Part 1 Solution: {total}")

    def get_total_valid_inputs(self, start: int, end: int) -> int:
        count = 0
        for value in range(start, end + 1):
            code = Code(value)
            if code.is_valid_code:
                print(value)
                count += 1
        return count

    def range_part_two(self):
        total = "Not Implemented"
        print(f"Part 2 Solution: {total}")


def main():
    aoc = AocFour()
    aoc.range_part_one()
    aoc.range_part_two()


if __name__ == "__main__":
    main()
