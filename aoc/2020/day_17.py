from timeit import timeit
from typing import Dict

TEST_INPUT = [
    ".#.",
    "..#",
    "###",
]

PUZZLE_INPUT = [
    "..#..#..",
    ".###..#.",
    "#..##.#.",
    "#.#.#.#.",
    ".#..###.",
    ".....#..",
    "#...####",
    "##....#.",
]


class Cube:
    def __init__(self, x: int, y: int, z: int, line_input: str):
        self.line_input = line_input
        self._active = "#" == line_input

        self.x = x
        self.y = y
        self.z = z

    @property
    def point(self) -> str:
        return f"{self.x},{self.y},{self.z}"

    @property
    def active(self) -> int:
        return 1 if self._active else 0


class Cubes:
    def __init__(self, cubes: Dict[str, int]):
        self.cubes = cubes

    @classmethod
    def from_line_generator(cls, line_generator):
        cubes = {}

        line_number = 0
        for line in line_generator:
            for index in range(len(line)):
                cube = Cube(x=index, y=line_number, z=0, line_input=line[index])
                if cube.active:
                    cubes[cube.point] = cube.active
            line_number += 1

        return cls(cubes)

    @property
    def active_cubes(self) -> int:
        active_count = 0
        for cube in self.cubes:
            active_count += self.cubes[cube]

        return active_count

    @property
    def next_day(self):
        cubes_assessed = set()
        cubes_to_pass = {}

        for cube in self.cubes:
            for adjacent_cube in self.adjacent_cubes(cube):
                if adjacent_cube in cubes_assessed:
                    continue

                active = self.cubes.get(adjacent_cube, 0)
                if self.flip_cube(adjacent_cube):
                    active = int(not active)

                if active:
                    cubes_to_pass[adjacent_cube] = active

                cubes_assessed.add(adjacent_cube)

        return Cubes(cubes_to_pass)

    def flip_cube(self, point: str) -> bool:
        cube_is_active = self.cubes.get(point, 0)
        if cube_is_active:
            return self.flip_active_cube(point)
        else:
            return self.flip_inactive_cube(point)

    def flip_active_cube(self, point: str) -> bool:
        number_of_adjacent_active_cubes = 0
        for adjacent_hexagon in self.adjacent_cubes(point, include_self=False):
            number_of_adjacent_active_cubes += self.cubes.get(adjacent_hexagon, 0)
            if number_of_adjacent_active_cubes > 3:
                return True

        return not (2 <= number_of_adjacent_active_cubes <= 3)

    def flip_inactive_cube(self, point: str) -> bool:
        number_of_adjacent_active_cubes = 0
        for adjacent_hexagon in self.adjacent_cubes(point, include_self=False):
            number_of_adjacent_active_cubes += self.cubes.get(adjacent_hexagon, 0)
            if number_of_adjacent_active_cubes > 3:
                return False

        return number_of_adjacent_active_cubes == 3

    def adjacent_cubes(self, point: str, include_self: bool = True):
        x, y, z = (int(coordinate) for coordinate in point.split(","))

        yield f"{x - 1},{y - 1},{z - 1}"
        yield f"{x - 1},{y - 1},{z}"
        yield f"{x - 1},{y - 1},{z + 1}"

        yield f"{x - 1},{y},{z - 1}"
        yield f"{x - 1},{y},{z}"
        yield f"{x - 1},{y},{z + 1}"

        yield f"{x - 1},{y + 1},{z - 1}"
        yield f"{x - 1},{y + 1},{z}"
        yield f"{x - 1},{y + 1},{z + 1}"

        yield f"{x},{y - 1},{z - 1}"
        yield f"{x},{y - 1},{z}"
        yield f"{x},{y - 1},{z + 1}"

        yield f"{x},{y},{z - 1}"
        if include_self:
            yield f"{x},{y},{z}"  # self
        yield f"{x},{y},{z + 1}"

        yield f"{x},{y + 1},{z - 1}"
        yield f"{x},{y + 1},{z}"
        yield f"{x},{y + 1},{z + 1}"

        yield f"{x + 1},{y - 1},{z - 1}"
        yield f"{x + 1},{y - 1},{z}"
        yield f"{x + 1},{y - 1},{z + 1}"

        yield f"{x + 1},{y},{z - 1}"
        yield f"{x + 1},{y},{z}"
        yield f"{x + 1},{y},{z + 1}"

        yield f"{x + 1},{y + 1},{z - 1}"
        yield f"{x + 1},{y + 1},{z}"
        yield f"{x + 1},{y + 1},{z + 1}"


class AocSeventeen:

    def __init__(self, test_case: bool = True):
        self.test_case = test_case
        if test_case:
            self.part_one_expected_result = 112
            self.part_two_expected_results = None
        else:
            self.part_one_expected_result = None
            self.part_two_expected_results = None

    def line_generator(self):
        if self.test_case:
            TEST_INPUT.reverse()
            for input_line in TEST_INPUT:
                yield input_line
        else:
            PUZZLE_INPUT.reverse()
            for input_line in PUZZLE_INPUT:
                yield input_line

    def part_one(self):
        """~75ms"""
        cubes = Cubes.from_line_generator(self.line_generator())
        for days in range(6):
            cubes = cubes.next_day

        # assert self.part_one_expected_result == cubes.active_cubes
        print(f"Part 1 solution: {cubes.active_cubes}")


def main():
    aoc = AocSeventeen(test_case=False)
    print(f"Problem 17 took {timeit(aoc.part_one, number=1)} seconds to execute")


if __name__ == "__main__":
    main()
