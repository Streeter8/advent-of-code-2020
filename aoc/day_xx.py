from timeit import timeit


class Aoc:
    """
    Template file for solutions
    """
    def part_one(self):
        total = "Not Implemented"
        print(f"Part 1 Solution: {total}")

    def part_two(self):
        total = "Not Implemented"
        print(f"Part 2 Solution: {total}")


def main():
    aoc = Aoc()
    print(f"Part one took {timeit(aoc.part_one, number=1)} seconds to execute")
    print(f"Part two took {timeit(aoc.part_two, number=1)} seconds to execute")


if __name__ == "__main__":
    main()
