from datetime import datetime, timedelta, timezone
from timeit import timeit

CUPS_SAMPLE = "389125467"
PUZZLE_INPUT = "925176834"
PART_ONE_MOVES = 100
PART_TWO_CUPS = 1000000
PART_TWO_MOVES = 10000000

CUPS = {}


class Cap:
    def __init__(self):
        self._value = None
        self._value_minus_one = None

    @property
    def value(self) -> int:
        if self._value is None:
            self._value_minus_one = len(CUPS)
            self._value = self._value_minus_one + 1

        return self._value

    @property
    def value_minus_one(self) -> int:
        return self._value_minus_one


CAP = Cap()


class Cup:
    def __init__(self, name: int, next_cup=None):
        self.name = name
        self.next_cup = next_cup

    def move(self):
        parent_popped_cup = self.next_cup

        self.next_cup = parent_popped_cup.next_cup.next_cup.next_cup

        destination = self.determine_destination(parent_popped_cup)

        CUPS[destination].insert(parent_popped_cup)

        return self.next_cup

    def determine_destination(self, parent_popped_cup) -> int:
        destination = self._determine_destination(self.name)

        while parent_popped_cup.contains_cup(destination):
            destination = self._determine_destination(destination)

        return destination

    def _determine_destination(self, destination: int) -> int:
        if (_destination := (destination - 1) % CAP.value) != 0:
            return _destination

        return CAP.value_minus_one

    def contains_cup(self, cup_name: int) -> bool:
        return (
            cup_name == self.name
            or cup_name == self.next_cup.name
            or cup_name == self.next_cup.next_cup.name
        )

    def insert(self, cup):
        cup.next_cup.next_cup.next_cup = self.next_cup
        self.next_cup = cup

    def debug(self, turn: int = 0):
        debug = f"{self.name}"
        next_cup = self.next_cup
        while next_cup.name != self.name:
            debug = f"{debug}{next_cup.name}"
            next_cup = next_cup.next_cup

        print(f"Turn {turn + 1}: {debug}")


class AocTwentyThree:
    def __init__(self, test_input: bool = True):
        if test_input:
            self.cups = CUPS_SAMPLE
            self.part_one_solution = "67384529"
            self.part_two_solution = 149245887792
        else:
            self.cups = PUZZLE_INPUT
            self.part_one_solution = "69852437"
            self.part_two_solution = 91408386135

    def part_one(self):
        """0.1ms"""
        current_cup = int(self.cups[0])
        previous_cup = Cup(current_cup)
        CUPS[current_cup] = previous_cup

        for _cup in self.cups[1:]:
            name = int(_cup)
            cup = Cup(name)
            previous_cup.next_cup = cup
            CUPS[name] = cup
            previous_cup = cup

        cup.next_cup = CUPS[current_cup]
        current_cup = CUPS[current_cup]

        for _turn in range(PART_ONE_MOVES):
            current_cup = current_cup.move()

        solution = ""
        next_cup = CUPS[1].next_cup
        while next_cup.name != 1:
            solution = f"{solution}{next_cup.name}"
            next_cup = next_cup.next_cup

        print(f"{solution=}")
        assert solution == self.part_one_solution

    def part_two(self):
        """~25 seconds"""
        current_cup = int(self.cups[0])
        previous_cup = Cup(current_cup)
        CUPS[current_cup] = previous_cup

        for _cup in self.cups[1:]:
            name = int(_cup)
            cup = Cup(name)
            previous_cup.next_cup = cup
            CUPS[name] = cup
            previous_cup = cup

        for _cup in range(10, PART_TWO_CUPS + 1):
            name = int(_cup)
            cup = Cup(name)
            previous_cup.next_cup = cup
            CUPS[name] = cup
            previous_cup = cup

        cup.next_cup = CUPS[current_cup]
        current_cup = CUPS[current_cup]

        beginning = self.now
        for _turn in range(PART_TWO_MOVES):
            if _turn % 1000000 == 0 and _turn != 0:
                delta = self.now - beginning
                total_time = delta.seconds + (delta.microseconds / 1000000)
                average_time = total_time / _turn
                finish_time = (self.now + timedelta(seconds=average_time) * (PART_TWO_MOVES - _turn)).isoformat()

                print(f"Executing turn {_turn}: Turns remaining: {PART_TWO_MOVES - _turn}")
                print(f"Total time to execute {_turn} turns: {total_time} seconds")
                print(f"Average time: {average_time} seconds per turn")
                print(f"Estimated Total Time: {average_time * PART_TWO_MOVES} seconds")
                print(f"Estimated Finish Time: {finish_time}")
                print("\n==================================================================\n")

            current_cup = current_cup.move()

        solution = CUPS[1].next_cup.name * CUPS[1].next_cup.next_cup.name
        print(f"{CUPS[1].next_cup.name=}")
        print(f"{CUPS[1].next_cup.next_cup.name=}")
        print(f"{solution=}")

        assert solution == self.part_two_solution

    @property
    def now(self) -> datetime:
        return datetime.now(timezone.utc)


def main():
    aoc = AocTwentyThree(test_input=False)
    # print(f"Part one took {timeit(aoc.part_one, number=1)} seconds to execute")
    print(f"Part two took {timeit(aoc.part_two, number=1)} seconds to execute")


if __name__ == "__main__":
    main()
