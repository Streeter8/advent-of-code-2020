import os
from timeit import timeit


class AocSix:
    DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    INPUT_FILE = "day_06.txt"

    def line_generator(self):
        input_file_path = os.path.join(self.DIRECTORY, "inputs", self.INPUT_FILE)
        with open(input_file_path) as input_file:
            for input_line in input_file:
                yield input_line.replace("\n", "")

    def six(self):
        """~3ms"""
        any_answers_count = 0
        all_answers_count = 0
        any_group_answers = set()
        all_group_answers = None

        for input_line in self.line_generator():
            if input_line:
                line = set(input_line)
                any_group_answers = any_group_answers.union(line)
                if all_group_answers is not None:
                    all_group_answers = all_group_answers.intersection(line)
                else:
                    all_group_answers = line
            else:
                any_answers_count += len(any_group_answers)
                all_answers_count += len(all_group_answers)
                any_group_answers = set()
                all_group_answers = None

        if any_group_answers:
            any_answers_count += len(any_group_answers)
        if all_group_answers:
            all_answers_count += len(all_group_answers)

        print(f"Part 1 Solution: {any_answers_count}")
        print(f"Part 2 Solution: {all_answers_count}")


def main():
    aoc = AocSix()
    print(f"Part one took {timeit(aoc.six, number=1)} seconds to execute")


if __name__ == "__main__":
    main()
