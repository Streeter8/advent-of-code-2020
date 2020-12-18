import os
from timeit import timeit


class AocNine:
    DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    INPUT_FILE = "day_09.txt"

    def __init__(self):
        self.allowed_numbers = set()

    def line_generator(self):
        input_file_path = os.path.join(self.DIRECTORY, "inputs", self.INPUT_FILE)
        with open(input_file_path) as input_file:
            for input_line in input_file:
                yield input_line.replace("\n", "")

    @property
    def _input(self) -> list:
        # return [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219, 299, 277, 309, 576]
        return [int(number) for number in self.line_generator()]

    @property
    def preamble(self) -> int:
        # return 5
        return 25

    def part_one(self):
        """~4ms"""
        # preamble = 5
        # self.set_allowed_sums(preamble, _input)
        first = self.find_first_invalid_number(self.preamble, self._input)
        print(f"The first invalid number is: {first}")

    def is_allowed_number(self, number: int, numbers: list):
        len_numbers = len(numbers)
        for index_one in range(len_numbers):
            for index_two in range(index_one, len_numbers):
                if number == numbers[index_one] + numbers[index_two]:
                    return True

        return False

    def find_first_invalid_number(self, preamble: int, _input: list) -> int:
        for index in range(preamble, len(_input)):
            if not self.is_allowed_number(_input[index], _input[index-preamble:index]):
                return _input[index]
        raise Exception("No invalid numbers found")


def main():
    aoc = AocNine()
    print(f"Part one took {timeit(aoc.part_one, number=1)} seconds to execute")


if __name__ == "__main__":
    main()
