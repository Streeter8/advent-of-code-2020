import os
from timeit import timeit
from typing import Dict


class Boat:
    DIRECTIONS_TURNS = {
        "E": {
            0: "E",
            90: "S",
            180: "W",
            270: "N",
        },
        "S": {
            0: "S",
            90: "W",
            180: "N",
            270: "E",
        },
        "W": {
            0: "W",
            90: "N",
            180: "E",
            270: "S",
        },
        "N": {
            0: "N",
            90: "E",
            180: "S",
            270: "W",
        },
    }

    LEFT_TO_RIGHT_DEGREES = {
        0: 0,
        90: 270,
        180: 180,
        270: 90,
    }

    TURN_COMMANDS = ("L", "R")

    def __init__(self):
        self.orientation = "E"
        self.x_pos = 0
        self.y_pos = 0

        self.go_methods: Dict[str, callable] = {
            "E": self.go_east,
            "S": self.go_south,
            "W": self.go_west,
            "N": self.go_north,
        }

    @property
    def manhattan_distance(self) -> int:
        return abs(self.x_pos) + abs(self.y_pos)

    def command(self, command: str, units: int):
        if command in self.TURN_COMMANDS:
            self.turn(command, units)
        elif command == "F":
            self.go_forward(units)
        else:
            self.go_methods[command](units)

    def turn(self, direction: str, _degrees: int):
        if direction == "L":
            degrees = self.LEFT_TO_RIGHT_DEGREES[_degrees]
        else:
            degrees = _degrees

        self.orientation = self.DIRECTIONS_TURNS[self.orientation][degrees]

    def go_forward(self, units: int):
        self.go_methods[self.orientation](units)

    def go_east(self, units: int):
        self.x_pos += units

    def go_west(self, units: int):
        self.x_pos -= units

    def go_north(self, units: int):
        self.y_pos += units

    def go_south(self, units: int):
        self.y_pos -= units


class AocTwelve:
    DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    INPUT_FILE = "day_12.txt"

    def part_one(self):
        boat = Boat()

        input_file_path = os.path.join(self.DIRECTORY, "inputs", self.INPUT_FILE)
        with open(input_file_path) as input_file:
            for input_line in input_file:
                command = input_line[0]
                units = int(input_line[1:])
                boat.command(command, units)

        print(f"{boat.x_pos=}, {boat.y_pos=}")
        print(f"Part 1 Solution: {boat.manhattan_distance}")


def main():
    aoc = AocTwelve()
    print(f"Part one took {timeit(aoc.part_one, number=1)} seconds to execute")


if __name__ == "__main__":
    main()
