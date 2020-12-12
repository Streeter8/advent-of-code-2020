import os
from timeit import timeit


class AocTwo:
    DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    INPUT_FILE = "day_02.txt"

    def part_one(self):
        """
        ~1ms
        """
        input_file_path = os.path.join(self.DIRECTORY, "inputs", self.INPUT_FILE)

        valid_passwords = 0
        with open(input_file_path) as input_file:
            for input_line in input_file:
                counts, _letter, password = input_line.split(" ")
                min_count, max_count = counts.split("-")
                letter = _letter[0]
                count = password.count(letter)
                if int(min_count) <= count <= int(max_count):
                    valid_passwords += 1

        print(f"Part 1 Solution: {valid_passwords}")

    def part_two(self):
        """
        ~1ms
        """
        input_file_path = os.path.join(self.DIRECTORY, "inputs", self.INPUT_FILE)

        valid_passwords = 0
        with open(input_file_path) as input_file:
            for input_line in input_file:
                indexes, _letter, password = input_line.split(" ")
                index_one, index_two = indexes.split("-")
                letter = _letter[0]
                letters = {password[int(index_one) - 1], password[int(index_two) - 1]}
                if letter in letters and len(letters) == 2:
                    valid_passwords += 1

        print(f"Part 2 Solution: {valid_passwords}")


def main():
    aoc = AocTwo()
    print(f"Part one took {timeit(aoc.part_one, number=1)} seconds to execute")
    print(f"Part two took {timeit(aoc.part_two, number=1)} seconds to execute")


if __name__ == "__main__":
    main()
