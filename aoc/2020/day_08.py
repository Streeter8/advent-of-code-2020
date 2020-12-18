import os
from timeit import timeit
from typing import List, Tuple


class Accumulator:

    def __init__(self, commands: List[Tuple[str, int]]):
        self.accumulator = 0
        self.command_index = 0
        self.commands = commands
        self.command_length = len(commands)
        self.executed_commands = set()

    def validate_commands(self):
        while self.command_index < self.command_length:
            if self.command_index in self.executed_commands:
                raise Exception

            self.executed_commands.add(self.command_index)
            command, value = self.commands[self.command_index]
            command_method = getattr(self, command)
            command_method(value)

    def nop(self, _: int):
        self.increment_command()

    def acc(self, accumulate: int):
        self.accumulator += accumulate
        self.increment_command()

    def increment_command(self):
        self.command_index += 1

    def jmp(self, index: int):
        self.command_index += index


class AocEight:
    DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    INPUT_FILE = "day_08.txt"

    def __init__(self):
        self.accumulator = 0
        self.command_index = 0

    def line_generator(self):
        input_file_path = os.path.join(self.DIRECTORY, "inputs", self.INPUT_FILE)
        with open(input_file_path) as input_file:
            for input_line in input_file:
                yield input_line.replace("\n", "")

        # lines = [
        #     "nop +0", "acc +1", "jmp +4", "acc +3", "jmp -3", "acc -99", "acc +1", "jmp -4", "acc +6"
        # ]
        # for line in lines:
        #     yield line

    @property
    def _input(self) -> List[Tuple[str, int]]:
        lines = []
        for line in self.line_generator():
            operation, value = line.split(" ")
            lines.append((operation, int(value)))

        return lines

    def corrected_input(self) -> List[Tuple[str, int]]:
        lines = self._input
        for index in range(len(lines)):
            if lines[index][0] == "jmp":
                yield self.generate_corrected_input(lines, index, "nop")
            if lines[index][0] == "nop":
                yield self.generate_corrected_input(lines, index, "jmp")

    def generate_corrected_input(
        self,
        lines: List[Tuple[str, int]],
        index: int,
        command: str
    ) -> List[Tuple[str, int]]:
        return (
            lines[:index]
            + [(command, lines[index][1])]
            + lines[index + 1:]
        )

    def part_one(self):
        """<1ms"""
        accumulator = Accumulator(self._input)
        try:
            accumulator.validate_commands()
        except Exception:
            print(f"Part 1 solution: {accumulator.accumulator}")

    def part_two(self):
        """~10ms"""
        for possible_input in self.corrected_input():
            accumulator = Accumulator(possible_input)
            try:
                accumulator.validate_commands()
            except Exception:
                continue

            print(f"Part 2 solution: {accumulator.accumulator}")
            break


def main():
    aoc = AocEight()
    print(f"Part one took {timeit(aoc.part_one, number=1)} seconds to execute")
    print(f"Part two took {timeit(aoc.part_two, number=1)} seconds to execute")


if __name__ == "__main__":
    main()
