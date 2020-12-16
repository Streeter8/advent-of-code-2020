import os
from timeit import timeit


class AocFive:
    DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    INPUT_FILE = "day_05.txt"

    def execute(self):
        """~2ms to fully execute"""
        input_file_path = os.path.join(self.DIRECTORY, "inputs", self.INPUT_FILE)

        seat_ids = set()
        with open(input_file_path) as input_file:
            for input_line in input_file:
                boarding_pass = input_line.replace("\n", "")
                seat_id = self.get_seat_id(boarding_pass)
                seat_ids.add(seat_id)

        max_seat_id = max(seat_ids)
        print(f"Part 1 Solution: Max Seat ID: {max_seat_id}")

        for seat_id in range(min(seat_ids), max_seat_id):
            if seat_id not in seat_ids:
                print(f"Part 2 Solution: My Seat ID: {seat_id}")
                break

        # I ran first without the break,
        # considering if there would be more than one empty seat.
        # There was only one empty seat though.
        # So we're just going to stop here and call it good.

    def get_seat_id(self, boarding_pass: str) -> int:
        """
        Convert values into bit strings, then cast to an integer
        """
        _row = boarding_pass[:7]
        _column = boarding_pass[7:]
        row = int("".join("1" if char == "B" else "0" for char in _row), 2)
        column = int("".join("1" if char == "R" else "0" for char in _column), 2)
        seat_id = row * 8 + column
        return seat_id


def main():
    aoc = AocFive()
    print(f"Day 5 Problem took {timeit(aoc.execute, number=1)} seconds to execute")


if __name__ == "__main__":
    main()
