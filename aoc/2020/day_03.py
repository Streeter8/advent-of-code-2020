import os
from timeit import timeit


class AocThree:
    DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    INPUT_FILE = "day_03.txt"

    def line_generator(self):
        input_file_path = os.path.join(self.DIRECTORY, "inputs", self.INPUT_FILE)
        with open(input_file_path) as input_file:
            for input_line in input_file:
                yield input_line.replace("\n", "")

        # test_inputs = [
        #     "..##.......\n",
        #     "#...#...#..\n",
        #     ".#....#..#.\n",
        #     "..#.#...#.#\n",
        #     ".#...##..#.\n",
        #     "..#.##.....\n",
        #     ".#.#.#....#\n",
        #     ".#........#\n",
        #     "#.##...#...\n",
        #     "#...##....#\n",
        #     ".#..#...#.#\n",
        # ]
        # for input_line in test_inputs:
        #     yield input_line.replace("\n", "")

    def part_one(self):
        """<1ms"""
        number_of_trees = self.determine_tree_count(x_slope=3, y_slope=1)
        print(f"Part 1 Solution: Total trees: {number_of_trees}")

    def part_two(self):
        """~1ms"""
        product = (
            self.determine_tree_count(x_slope=1, y_slope=1)
            * self.determine_tree_count(x_slope=3, y_slope=1)
            * self.determine_tree_count(x_slope=5, y_slope=1)
            * self.determine_tree_count(x_slope=7, y_slope=1)
            * self.determine_tree_count(x_slope=1, y_slope=2)
        )

        print(f"Part 2 Solution: {product}")

    def determine_tree_count(self, x_slope: int, y_slope: int) -> int:
        x_coordinate = -1 * x_slope
        line_count = 0

        number_of_trees = 0
        for input_line in self.line_generator():
            if line_count % y_slope == 0:
                x_coordinate = (x_coordinate + x_slope) % (len(input_line))
                if input_line[x_coordinate] == "#":
                    number_of_trees += 1

            line_count += 1

        return number_of_trees


def main():
    aoc = AocThree()
    print(f"Part one took {timeit(aoc.part_one, number=1)} seconds to execute")
    print(f"Part two took {timeit(aoc.part_two, number=1)} seconds to execute")


if __name__ == "__main__":
    main()
