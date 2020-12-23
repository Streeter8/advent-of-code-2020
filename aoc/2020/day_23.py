from timeit import timeit
from typing import List

CUPS_SAMPLE = "389125467"
PUZZLE_INPUT = "925176834"
PART_ONE_MOVES = 100
PART_TWO_CUPS = 1000000
PART_TWO_MOVES = 10000000


class AocTwentyThree:
    def __init__(self):
        self.cups = CUPS_SAMPLE

    def part_one(self):
        """0.1ms"""
        cups = [int(cup) for cup in self.cups]
        number_of_cups = len(cups)
        for _turn in range(PART_ONE_MOVES):
            cups = self.move(cups, number_of_cups)

        cups_after_one = self.apply_one_shift(cups)

        solution = "".join(str(cup) for cup in cups_after_one)
        print(f"Part one solution: {solution}")

    def part_two(self):
        cups = [int(cup) for cup in self.cups]
        cups = cups + [cup for cup in range(max(cups), PART_TWO_CUPS + 1)]
        number_of_cups = len(cups)
        for _turn in range(PART_TWO_MOVES):
            if _turn % 100 == 0:
                print(f"Executing turn {_turn}: Turns remaining: {PART_TWO_MOVES - _turn}")
            cups = self.move(cups, number_of_cups)

        cups_after_one = self.apply_one_shift(cups)

        solution = cups_after_one[0] * cups_after_one[1]
        print(f"Part two solution: {solution}")

    def move(self, cups: List[int], number_of_cups: int) -> List[int]:
        current_cup = cups[0]
        pick_up = cups[1:4]
        remaining_cups = cups[:1] + cups[4:]
        destination = self.determine_destination(current_cup, remaining_cups, number_of_cups)
        index = remaining_cups.index(destination)
        new_cups = remaining_cups[0: index + 1] + pick_up + remaining_cups[index + 1:len(remaining_cups)]

        # moving first cup to the end 'shifts' the current cup for the next turn
        result = new_cups[1:] + new_cups[:1]
        return result

    def determine_destination(self, current_cup: int, remaining_cups: List[int], number_of_cups: int) -> int:
        destination = (current_cup - 1) % (number_of_cups + 1)
        while destination not in remaining_cups:
            destination = (destination - 1) % (number_of_cups + 1)

        return destination

    def apply_one_shift(self, cups):
        one_index = cups.index(1)
        cups_after_one = cups[one_index + 1:len(cups)] + cups[0:one_index]
        return cups_after_one


def main():
    aoc = AocTwentyThree()
    print(f"Part one took {timeit(aoc.part_one, number=1)} seconds to execute")
    print(f"Part two took {timeit(aoc.part_two, number=1)} seconds to execute")


if __name__ == "__main__":
    main()
