import os
from timeit import timeit
from typing import Dict


class Waypoint:
    TURN_COMMANDS = ("L", "R")

    def __init__(self):
        self.x_pos = 10
        self.y_pos = 1

        self.go_methods: Dict[str, callable] = {
            "E": self.go_east,
            "S": self.go_south,
            "W": self.go_west,
            "N": self.go_north,
        }
        self.left_turns = {
            90: self.turn_270,
            180: self.turn_180,
            270: self.turn_90,
        }
        self.right_turns = {
            90: self.turn_90,
            180: self.turn_180,
            270: self.turn_270,
        }

    def command(self, command: str, units: int):
        if command in self.TURN_COMMANDS:
            self.turn(command, units)
        else:
            self.go_methods[command](units)

    def turn(self, direction: str, degrees: int):
        if direction == "L":
            self.left_turns[degrees]()
        else:
            self.right_turns[degrees]()

    def turn_90(self):
        x_pos = self.x_pos
        self.x_pos = self.y_pos
        self.y_pos = -1 * x_pos

    def turn_180(self):
        self.x_pos = -1 * self.x_pos
        self.y_pos = -1 * self.y_pos

    def turn_270(self):
        x_pos = self.x_pos
        self.x_pos = -1 * self.y_pos
        self.y_pos = x_pos

    def go_east(self, units: int):
        self.x_pos += units

    def go_west(self, units: int):
        self.x_pos -= units

    def go_north(self, units: int):
        self.y_pos += units

    def go_south(self, units: int):
        self.y_pos -= units


class Boat:
    def __init__(self):
        self.x_pos = 0
        self.y_pos = 0
        self.waypoint = Waypoint()

    @property
    def manhattan_distance(self) -> int:
        return abs(self.x_pos) + abs(self.y_pos)

    def command(self, command: str, units: int):
        if command == "F":
            self.go_forward(units)
        else:
            self.waypoint.command(command, units)

    def go_forward(self, units: int):
        self.x_pos += self.waypoint.x_pos * units
        self.y_pos += self.waypoint.y_pos * units


class AocTwelvePartTwo:
    DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    INPUT_FILE = "day_12.txt"

    def part_two(self):
        """
        ~1ms
        """
        boat = Boat()

        input_file_path = os.path.join(self.DIRECTORY, "inputs", self.INPUT_FILE)
        with open(input_file_path) as input_file:
            for input_line in input_file:
                command = input_line[0]
                units = int(input_line[1:])
                boat.command(command, units)

        print(f"{boat.x_pos=}, {boat.y_pos=}")
        print(f"Part 2 Solution: {boat.manhattan_distance}")


def main():
    aoc = AocTwelvePartTwo()
    print(f"Part two took {timeit(aoc.part_two, number=1)} seconds to execute")


if __name__ == "__main__":
    main()
