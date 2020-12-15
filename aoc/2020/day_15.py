from timeit import timeit
from typing import List

INPUT = [3, 1, 2]
PUZZLE_INPUT = [18, 8, 0, 5, 4, 1, 20]


class MemoryGameSimple:
    """
    This was my initial attempt at the problem.
    It worked just fine for part one.
    But the size of part two seemed to be a bit too much
    for the 30 million request for part two.
    """

    def __init__(self, initial_input: List[int]):
        self.numbers = [number for number in initial_input]
        self.reversed_numbers = [number for number in initial_input]
        self.reversed_numbers.reverse()

    def generate_next(self) -> None:
        self.insert(self.last_occurrence_of_number)

    @property
    def last_number(self) -> int:
        return self.numbers[-1]

    @property
    def previous_numbers(self) -> List[int]:
        return self.numbers[:-1]

    @property
    def last_number_was_said_before(self) -> bool:
        return self.last_number in self.previous_numbers

    @property
    def last_occurrence_of_number(self) -> int:
        if not self.last_number_was_said_before:
            return 0

        current_turn_number = len(self.numbers)
        most_recent_turn_number = current_turn_number - self.reversed_numbers[1:].index(self.last_number) - 1
        return current_turn_number - most_recent_turn_number

    def get_index(self, index: int):
        while len(self.numbers) < index:
            self.generate_next()

        return self.numbers[index - 1]

    def insert(self, number: int) -> None:
        self.numbers.append(number)
        self.reversed_numbers.insert(0, number)


class MemoryGame:
    """
    We optimized this object by realizing that
    we didn't need to remember when every number had ever been said.
    Instead, we just need to remember only the last time each number was said.
    This keeps us from storing and searching large lists in memory.
    """

    def __init__(self, initial_input: List[int]):
        self.current_number = None
        self.numbers = {}
        self.said_before = set()

        for index in range(len(initial_input)):
            turn = index + 1
            self.numbers[initial_input[index]] = turn
            self.current_turn = turn
            self.current_number = initial_input[index]

        del self.numbers[initial_input[-1]]

    def generate_next(self) -> None:
        next_number = 0
        if self.current_number in self.numbers:
            next_number = self.current_turn - self.numbers[self.current_number]

        self.numbers[self.current_number] = self.current_turn
        # if 0 == self.current_turn % 200000:
        #     print(f"{self.current_turn}: {next_number}")

        self.current_turn += 1
        self.current_number = next_number

    def get_turn(self, turn: int):
        while self.current_turn < turn:
            self.generate_next()

        return self.current_number


class AocFifteen:
    def part_one_a(self):
        """'Simple' approach took ~15ms"""
        game = MemoryGameSimple(PUZZLE_INPUT)
        turn = 2020
        number = game.get_index(turn)
        print(f"Part 1 Solution: {number}")

    def part_one_b(self):
        """'Advanced' approach took ~1.5ms"""
        game = MemoryGame(PUZZLE_INPUT)
        turn = 2020
        number = game.get_turn(turn)
        print(f"Part 1 Solution: {number}")

    def part_two(self):
        """
        'Simple' approach didn't finish in under 30 minutes.
        So I pivoted to the 'advanced' approach, which took ~25 seconds
        """
        game = MemoryGame(PUZZLE_INPUT)
        turn = 30000000
        number = game.get_turn(turn)

        print(f"Part 2 Solution: {number}")


def main():
    aoc = AocFifteen()
    print(f"Part one a took {timeit(aoc.part_one_a, number=1)} seconds to execute")
    print(f"Part one b took {timeit(aoc.part_one_b, number=1)} seconds to execute")
    print(f"Part two took {timeit(aoc.part_two, number=1)} seconds to execute")


if __name__ == "__main__":
    main()
