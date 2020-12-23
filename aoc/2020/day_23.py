from timeit import timeit
from typing import List

CUPS_SAMPLE = "389125467"
PUZZLE_INPUT = "925176834"


class AocTwentyThree:
    def __init__(self, turns: int = 10):
        # self.cups = [int(cup) for cup in CUPS_SAMPLE]
        self.cups = [int(cup) for cup in PUZZLE_INPUT]
        self.turns = turns

    def part_one(self):
        """0.1ms"""
        cups = self.cups
        for _turn in range(self.turns):
            cups = self.move(cups)

        one_index = cups.index(1)
        cups_after_one = cups[one_index + 1:len(cups)] + cups[0:one_index]

        solution = "".join(str(cup) for cup in cups_after_one)
        print(f"Part one solution: {solution}")

    def move(self, cups: List[int]) -> List[int]:
        current_cup = cups[0]
        pick_up = cups[1:4]
        remaining_cups = cups[:1] + cups[4:]
        destination = self.determine_destination(current_cup, remaining_cups)
        index = remaining_cups.index(destination)
        new_cups = remaining_cups[0: index + 1] + pick_up + remaining_cups[index + 1:len(remaining_cups)]

        # moving first cup to the end 'shifts' the current cup for the next turn
        result = new_cups[1:] + new_cups[:1]
        return result

    def determine_destination(self, current_cup: int, remaining_cups: List[int]) -> int:
        destination = (current_cup - 1) % 10
        while destination not in remaining_cups:
            destination = (destination - 1) % 10

        return destination

    def part_two(self):
        pass


def main():
    aoc = AocTwentyThree(turns=100)
    print(f"Part one took {timeit(aoc.part_one, number=1)} seconds to execute")
    # print(f"Part two took {timeit(aoc.part_two, number=1)} seconds to execute")


if __name__ == "__main__":
    main()
