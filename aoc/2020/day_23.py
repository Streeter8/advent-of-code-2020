from datetime import datetime, timezone
from timeit import timeit
from typing import List

CUPS_SAMPLE = "389125467"
PUZZLE_INPUT = "925176834"
PART_ONE_MOVES = 100
PART_TWO_CUPS = 1000000
PART_TWO_MOVES = 10000000


class AocTwentyThree:
    def __init__(self, test_input: bool = True):
        if test_input:
            self.cups = CUPS_SAMPLE
            self.part_one_solution = "67384529"
        else:
            self.cups = PUZZLE_INPUT
            self.part_one_solution = "69852437"

    def part_one(self):
        """0.1ms"""
        cups = [int(cup) for cup in self.cups]
        number_of_cups = len(cups)
        for _turn in range(PART_ONE_MOVES):
            cups = self.move(cups, number_of_cups)

        cups_after_one = self.apply_one_shift(cups)

        solution = "".join(str(cup) for cup in cups_after_one)
        assert self.part_one_solution == solution
        print(f"Part one solution: {solution}")

    def part_two(self):
        cups = [int(cup) for cup in self.cups]
        cups.extend([cup for cup in range(max(cups) + 1, PART_TWO_CUPS + 1)])
        number_of_cups = len(cups)
        beginning = self.now
        for _turn in range(PART_TWO_MOVES):
            if _turn % 100 == 0 and _turn != 0:
                delta = self.now - beginning
                total_time = delta.seconds + (delta.microseconds / 1000000)
                average_time = total_time / _turn

                print(f"Executing turn {_turn}: Turns remaining: {PART_TWO_MOVES - _turn}")
                print(f"Total time to execute {_turn} turns: {total_time} seconds")
                print(f"Average time: {average_time} seconds per turn")
                print(f"\n==================================================================\n")

            cups = self.move(cups, number_of_cups)

        cups_after_one = self.apply_one_shift(cups)

        solution = cups_after_one[0] * cups_after_one[1]
        print(f"Part two solution: {solution}")

    def move(self, cups: List[int], number_of_cups: int) -> List[int]:
        # current_cup = cups[0]
        # pick_up = cups[1:4]
        pick_up = [cups.pop(1), cups.pop(1), cups.pop(1)]

        # remaining_cups = cups[:1] + cups[4:]
        # del cups[3]
        # del cups[2]
        # del cups[1]

        destination = self.determine_destination(cups[0], pick_up, number_of_cups + 1)
        index = cups.index(destination)

        # new_cups = cups[0: index + 1] + pick_up + cups[index + 1:number_of_cups - 3]
        cups.insert(index + 1, pick_up[2])
        cups.insert(index + 1, pick_up[1])
        cups.insert(index + 1, pick_up[0])

        # moving first cup to the end 'shifts' the current cup for the next turn
        # result = new_cups[1:] + new_cups[:1]
        cups.append(cups.pop(0))
        return cups

    def determine_destination(self, current_cup: int, picked_up_cups: List[int], cap: int) -> int:
        destination = self._determine_destination(current_cup, cap)

        while destination in picked_up_cups:
            destination = self._determine_destination(destination, cap)

        return destination

    def _determine_destination(self, destination: int, cap: int) -> int:
        if (_destination := (destination - 1) % cap) != 0:
            return _destination

        return cap - 1

    def apply_one_shift(self, cups):
        one_index = cups.index(1)
        cups_after_one = cups[one_index + 1:len(cups)] + cups[0:one_index]
        return cups_after_one

    @property
    def now(self) -> datetime:
        return datetime.now(timezone.utc)


def main():
    aoc = AocTwentyThree()
    print(f"Part one took {timeit(aoc.part_one, number=1)} seconds to execute")
    print(f"Part two took {timeit(aoc.part_two, number=1)} seconds to execute")


if __name__ == "__main__":
    main()
