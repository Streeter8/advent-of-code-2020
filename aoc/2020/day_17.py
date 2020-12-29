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


class Hypercube(Cube):
    def __init__(self, x: int, y: int, z: int, line_input: str):
        super().__init__(x, y, z, line_input)
        self.w = 0

    @property
    def point(self) -> str:
        return f"{self.x},{self.y},{self.z},{self.w}"


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

        return self.new_cube(cubes_to_pass)

    @classmethod
    def new_cube(cls, cubes: Dict[str, int]):
        return cls(cubes)

    def flip_cube(self, point: str) -> bool:
        cube_is_active = self.cubes.get(point, 0)
        if cube_is_active:
            return self.flip_active_cube(point)
        else:
            return self.flip_inactive_cube(point)

    def flip_active_cube(self, point: str) -> bool:
        number_of_adjacent_active_cubes = 0
        for adjacent_cube in self.adjacent_cubes(point):
            if adjacent_cube == point:
                # exclude self in evaluation
                continue

            number_of_adjacent_active_cubes += self.cubes.get(adjacent_cube, 0)
            if number_of_adjacent_active_cubes > 3:
                # Deactivate cube when more than 3 neighbors are active
                return True

        # Do not deactivate cube when exactly 2 or 3 neighbors are active
        return not (
            number_of_adjacent_active_cubes == 2
            or number_of_adjacent_active_cubes == 3
        )

    def flip_inactive_cube(self, point: str) -> bool:
        number_of_adjacent_active_cubes = 0
        for adjacent_cube in self.adjacent_cubes(point):
            if adjacent_cube == point:
                # exclude self in evaluation
                continue

            number_of_adjacent_active_cubes += self.cubes.get(adjacent_cube, 0)
            if number_of_adjacent_active_cubes > 3:
                # Do not activate cube when more than 3 neighbors are active
                return False

        # Activate inactive cube when exactly 3 neighbors are active
        return number_of_adjacent_active_cubes == 3

    def adjacent_cubes(self, point: str):
        x, y, z = (int(coordinate) for coordinate in point.split(","))
        for cube in self._adjacent_cubes(x, y, z):
            yield cube

    def _adjacent_cubes(self, x: int, y: int, z: int):
        for _x in range(x - 1, x + 2):
            for _y in range(y - 1, y + 2):
                for _z in range(z - 1, z + 2):
                    yield f"{_x},{_y},{_z}"


class Hypercubes(Cubes):
    @classmethod
    def from_line_generator(cls, line_generator):
        hypercubes = {}

        line_number = 0
        for line in line_generator:
            for index in range(len(line)):
                cube = Hypercube(x=index, y=line_number, z=0, line_input=line[index])
                if cube.active:
                    hypercubes[cube.point] = cube.active
            line_number += 1

        return cls(hypercubes)

    def adjacent_cubes(self, point: str, include_self: bool = True):
        x, y, z, w = (int(coordinate) for coordinate in point.split(","))
        for _w in range(w - 1, w + 2):
            for cube in self._adjacent_cubes(x, y, z):
                yield f"{cube},{_w}"


class AocSeventeen:

    def __init__(self, test_case: bool = True):
        self.test_case = test_case
        if test_case:
            self.part_one_expected_result = 112
            self.part_two_expected_result = 848
        else:
            self.part_one_expected_result = 242
            self.part_two_expected_result = None

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
        """~100ms"""
        cubes = Cubes.from_line_generator(self.line_generator())
        for day in range(6):
            cubes = cubes.next_day

        if self.part_one_expected_result:
            assert self.part_one_expected_result == cubes.active_cubes
        print(f"Part 1 solution: {cubes.active_cubes}")

    def part_two(self):
        """~2.75s"""
        hypercubes = Hypercubes.from_line_generator(self.line_generator())
        for day in range(6):
            hypercubes = hypercubes.next_day

        if self.part_two_expected_result:
            assert self.part_two_expected_result == hypercubes.active_cubes

        print(f"Part 2 solution: {hypercubes.active_cubes}")


def main():
    aoc = AocSeventeen(test_case=False)
    print(f"Part 1 took {timeit(aoc.part_one, number=1)} seconds to execute")
    print(f"Part 2 took {timeit(aoc.part_two, number=1)} seconds to execute")


if __name__ == "__main__":
    main()
