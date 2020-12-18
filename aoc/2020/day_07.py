import os
from timeit import timeit
from typing import List

BAGS = {}


class Bag:
    def __init__(self, line: str):
        name, contents = line.split(" bags contain ")
        self.name = name.replace(" bags", "").replace(" bag", "")
        self.contents = {}

        contents = contents.replace(".", "")
        if contents != "no other bags":
            for bag in contents.split(", "):
                number, bag_name = bag.split(" ", 1)
                bag_name = bag_name.replace(" bags", "").replace(" bag", "")
                self.contents[bag_name] = int(number)

    @property
    def can_contains_at_least_one_shiny_gold_bag(self) -> True:
        if "shiny gold" in self.contents:
            return True

        for bag in self.contents:
            if BAGS[bag].can_contains_at_least_one_shiny_gold_bag:
                return True

        return False

    @property
    def total_bags(self) -> int:
        if not self.contents:
            return 0

        total = 0
        for bag in self.contents:
            total_child_bags = BAGS[bag].total_bags
            if total_child_bags:
                _bags = self.contents[bag] * total_child_bags
            else:
                _bags = self.contents[bag]
            total += _bags

        return total + 1


class AocSeven:
    DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    INPUT_FILE = "day_07.txt"

    def __init__(self):
        self.accumulator = 0
        self.command_index = 0

    def line_generator(self):
        input_file_path = os.path.join(self.DIRECTORY, "inputs", self.INPUT_FILE)
        with open(input_file_path) as input_file:
            for input_line in input_file:
                yield input_line.replace("\n", "")

        # lines = [
        #     "light red bags contain 1 bright white bag, 2 muted yellow bags.",
        #     "dark orange bags contain 3 bright white bags, 4 muted yellow bags.",
        #     "bright white bags contain 1 shiny gold bag.",
        #     "muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.",
        #     "shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.",
        #     "dark olive bags contain 3 faded blue bags, 4 dotted black bags.",
        #     "vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.",
        #     "faded blue bags contain no other bags.",
        #     "dotted black bags contain no other bags.",
        # ]
        # for line in lines:
        #     yield line

    @property
    def _input(self) -> List[str]:
        return [line for line in self.line_generator()]

    def seven(self):
        """~35ms"""
        for line in self._input:
            bag = Bag(line)
            BAGS[bag.name] = bag

        print(f"Total bags within a shiny gold bag: {BAGS['shiny gold'].total_bags - 1}")

        total_bags = 0
        for bag in BAGS:
            if BAGS[bag].can_contains_at_least_one_shiny_gold_bag:
                total_bags += 1

        print(f"Total bags that can contain a shiny gold bag: {total_bags}")


def main():
    aoc = AocSeven()
    print(f"Problem seven took {timeit(aoc.seven, number=1)} seconds to execute")


if __name__ == "__main__":
    main()
