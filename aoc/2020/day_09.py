import os
from timeit import timeit
from typing import List


class AocNine:
    DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    INPUT_FILE = "day_09.txt"

    def __init__(self):
        self.invalid_number = None

    def line_generator(self):
        input_file_path = os.path.join(self.DIRECTORY, "inputs", self.INPUT_FILE)
        with open(input_file_path) as input_file:
            for input_line in input_file:
                yield input_line.replace("\n", "")

    @property
    def _input(self) -> List[int]:
        # return [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219, 299, 277, 309, 576]
        return [int(number) for number in self.line_generator()]

    @property
    def preamble(self) -> int:
        # return 5
        return 25

    def nine(self):
        """~20ms"""
        self.set_invalid_number(self.preamble, self._input)
        weak = self.find_encryption_weakness(self._input)
        print(f"Encryption weakness is: {weak}")

    def is_allowed_number(self, number: int, numbers: list) -> bool:
        len_numbers = len(numbers)
        for index_one in range(len_numbers):
            for index_two in range(index_one + 1, len_numbers):
                if number == numbers[index_one] + numbers[index_two]:
                    return True

        return False

    def set_invalid_number(self, preamble: int, _input: list) -> None:
        for index in range(preamble, len(_input)):
            if not self.is_allowed_number(_input[index], _input[index - preamble:index]):
                print(f"The first invalid number is: {_input[index]}")
                self.invalid_number = _input[index]
                break

    def find_encryption_weakness(self, _input: list) -> int:
        if not self.invalid_number:
            raise Exception("Invalid number not set")

        len_numbers = len(_input)
        for index_one in range(len_numbers):
            running_sum = _input[index_one]
            for index_two in range(index_one + 1, len_numbers):
                running_sum += _input[index_two]
                if running_sum == self.invalid_number:
                    return min(_input[index_one:index_two + 1]) + max(_input[index_one:index_two + 1])
                if running_sum > self.invalid_number:
                    break


def main():
    aoc = AocNine()
    print(f"Problem 9 took {timeit(aoc.nine, number=1)} seconds to execute")


if __name__ == "__main__":
    main()
