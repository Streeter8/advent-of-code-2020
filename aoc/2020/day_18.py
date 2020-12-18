import json
import os
from timeit import timeit


class ArithmeticFactory:
    def __init__(self, math_input: str):
        self.math_input = math_input

    def make(self):
        new_input = self.math_input.replace(
            "(", "["
        ).replace(
            ")", "]"
        ).replace(
            "+", '"+"'
        ).replace(
            "*", '"*"'
        ).replace(
            " ", ","
        )

        return self.analyze(json.loads(f"[{new_input}]"))

    def analyze(self, json_input: list):
        return self._analyze(json_input)

    def _analyze(self, json_input: list):
        running_total = 0
        operation = "set"

        for _input in json_input:
            if isinstance(_input, list):
                result = self.analyze(_input)
                running_total = self.perform_operation(running_total, result, operation)
            elif isinstance(_input, int):
                running_total = self.perform_operation(running_total, _input, operation)
            elif isinstance(_input, str):
                operation = _input
            else:
                raise Exception(f"Unexpected input type received: {_input}")

        return running_total

    def perform_operation(self, running_total, _input, operation):
        if operation == "set":
            return _input
        elif operation == "+":
            return running_total + _input
        elif operation == "*":
            return running_total * _input
        else:
            raise Exception(f"invalid operation provided: {operation}")


class ArithmeticFactoryAdvanced(ArithmeticFactory):
    def analyze(self, json_input: list) -> int:
        while "+" in json_input:
            index = json_input.index("+")
            left = json_input[index - 1]
            right = json_input[index + 1]
            if isinstance(left, list):
                left = self.analyze(left)
            if isinstance(right, list):
                right = self.analyze(right)

            json_input[index] = left + right
            del json_input[index + 1]
            del json_input[index - 1]

        return self._analyze(json_input)

    def perform_operation(self, running_total, _input, operation):
        if operation == "set":
            return _input
        elif operation == "*":
            return running_total * _input
        else:
            raise Exception(f"invalid operation provided: {operation}")


class AocEighteen:
    DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    INPUT_FILE = "day_18.txt"

    def line_generator(self):
        input_file_path = os.path.join(self.DIRECTORY, "inputs", self.INPUT_FILE)
        with open(input_file_path) as input_file:
            for input_line in input_file:
                yield input_line.replace("\n", "")

        # test_inputs = [
        #     "2 * 3 + (4 * 5)\n",
        #     "5 + (8 * 3 + 9 + 3 * 4 * 3)\n",
        #     "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))\n",
        #     "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2\n",
        # ]
        # for input_line in test_inputs:
        #     yield input_line.replace("\n", "")

    def part_one(self):
        """~5ms"""
        total = sum(
            ArithmeticFactory(input_line).make()
            for input_line in self.line_generator()
        )

        print(f"Part 1 Solution: {total}")

    def part_two(self):
        """~5ms"""
        total = sum(
            ArithmeticFactoryAdvanced(input_line).make()
            for input_line in self.line_generator()
        )

        print(f"Part 2 Solution: {total}")


def main():
    aoc = AocEighteen()
    print(f"Part one took {timeit(aoc.part_one, number=1)} seconds to execute")
    print(f"Part two took {timeit(aoc.part_two, number=1)} seconds to execute")


if __name__ == "__main__":
    main()
