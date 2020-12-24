import os
from timeit import timeit
from typing import Dict

NUMBER_OF_DAYS = 100
TERMINATOR_DIRECTIONS = {"e", "w"}


class Hexagon:
    def __init__(self, line_input: str):
        self.line_input = line_input

        self.x = 0
        self.y = 0

        self.directions = []

        direction = ""

        for character in line_input:
            direction = f"{direction}{character}"

            if character in TERMINATOR_DIRECTIONS:
                self._move_point(direction)

                self.directions.append(direction)
                direction = ""

    @property
    def point(self) -> str:
        return f"{self.x},{self.y}"

    def _move_point(self, direction: str):
        if len(direction) == 1:
            self._move_laterally(direction, 2)
        elif len(direction) == 2:
            self._move_diagonally(direction)
        else:
            raise Exception(f"Unexpected direction provided: {direction}")

    def _move_diagonally(self, direction: str):
        self._move_vertically(direction[0])
        self._move_laterally(direction[1], 1)

    def _move_laterally(self, direction: str, distance: int):
        if direction == "e":
            self.x += distance
        elif direction == "w":
            self.x -= distance
        else:
            raise Exception(f"Unexpected direction provided: {direction}")

    def _move_vertically(self, direction: str):
        if direction[0] == "n":
            self.y += 1
        elif direction == "s":
            self.y -= 1
        else:
            raise Exception(f"Unexpected direction provided: {direction}")


class Hexagons:
    def __init__(self, hexagons: Dict[str, int]):
        self.hexagons = hexagons

    @classmethod
    def from_line_generator(cls, line_generator):
        hexagons = {}

        for line in line_generator:
            hexagon = Hexagon(line)

            if hexagons.get(hexagon.point, 0):
                hexagons[hexagon.point] = 0
            else:
                hexagons[hexagon.point] = 1

        return cls(hexagons)

    @property
    def number_of_black_tiles(self) -> int:
        number_of_black_tiles = 0
        for hexagon in self.hexagons:
            number_of_black_tiles += self.hexagons[hexagon]

        return number_of_black_tiles

    @property
    def next_day(self):
        new_hexagons = {}

        for hexagon in self.hexagons:
            for adjacent_hexagon in self.adjacent_hexagons(hexagon):
                if adjacent_hexagon in new_hexagons:
                    continue

                color = self.hexagons.get(adjacent_hexagon, 0)
                if self.flip_tile(adjacent_hexagon):
                    new_hexagons[adjacent_hexagon] = int(not color)
                else:
                    new_hexagons[adjacent_hexagon] = color

        return Hexagons(new_hexagons)

    def flip_tile(self, point: str) -> bool:
        current_tile_is_black = self.hexagons.get(point, 0)
        if current_tile_is_black:
            return self.flip_black_tile(point)
        else:
            return self.flip_white_tile(point)

    def flip_black_tile(self, point: str) -> bool:
        number_of_adjacent_black_tiles = 0
        for adjacent_hexagon in self.adjacent_hexagons(point, include_self=False):
            number_of_adjacent_black_tiles += self.hexagons.get(adjacent_hexagon, 0)

        return (
            number_of_adjacent_black_tiles == 0
            or number_of_adjacent_black_tiles > 2
        )

    def flip_white_tile(self, point: str) -> bool:
        number_of_adjacent_black_tiles = 0
        for adjacent_hexagon in self.adjacent_hexagons(point, include_self=False):
            number_of_adjacent_black_tiles += self.hexagons.get(adjacent_hexagon, 0)

        return number_of_adjacent_black_tiles == 2

    def adjacent_hexagons(self, point: str, include_self: bool = True):
        x, y = (int(coordinate) for coordinate in point.split(","))

        yield f"{x - 1},{y + 1}"  # nw
        yield f"{x + 1},{y + 1}"  # ne
        yield f"{x + 2},{y}"  # e
        yield f"{x + 1},{y - 1}"  # se
        yield f"{x - 1},{y - 1}"  # sw
        yield f"{x - 2},{y}"  # w
        if include_self:
            yield f"{x},{y}"  # self


class AocTwentyFour:
    DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    INPUT_FILE = "day_24.txt"

    def __init__(self, test_case: bool = True):
        self.test_case = test_case
        if test_case:
            self.part_one_expected_result = 10
            self.part_two_expected_results = {
                1: 15,
                2: 12,
                3: 25,
                4: 14,
                5: 23,
                6: 28,
                7: 41,
                8: 37,
                9: 49,
                10: 37,
                20: 132,
                30: 259,
                40: 406,
                50: 566,
                60: 788,
                70: 1106,
                80: 1373,
                90: 1844,
                100: 2208,
            }
        else:
            self.part_one_expected_result = 495
            self.part_two_expected_results = {}

    def line_generator(self):
        if self.test_case:
            lines = [
                "sesenwnenenewseeswwswswwnenewsewsw\n",
                "neeenesenwnwwswnenewnwwsewnenwseswesw\n",
                "seswneswswsenwwnwse\n",
                "nwnwneseeswswnenewneswwnewseswneseene\n",
                "swweswneswnenwsewnwneneseenw\n",
                "eesenwseswswnenwswnwnwsewwnwsene\n",
                "sewnenenenesenwsewnenwwwse\n",
                "wenwwweseeeweswwwnwwe\n",
                "wsweesenenewnwwnwsenewsenwwsesesenwne\n",
                "neeswseenwwswnwswswnw\n",
                "nenwswwsewswnenenewsenwsenwnesesenew\n",
                "enewnwewneswsewnwswenweswnenwsenwsw\n",
                "sweneswneswneneenwnewenewwneswswnese\n",
                "swwesenesewenwneswnwwneseswwne\n",
                "enesenwswwswneneswsenwnewswseenwsese\n",
                "wnwnesenesenenwwnenwsewesewsesesew\n",
                "nenewswnwewswnenesenwnesewesw\n",
                "eneswnwswnwsenenwnwnwwseeswneewsenese\n",
                "neswnwewnwnwseenwseesewsenwsweewe\n",
                "wseweeenwnesenwwwswnew\n",
            ]
            for input_line in lines:
                yield input_line.replace("\n", "")
        else:
            input_file_path = os.path.join(self.DIRECTORY, "inputs", self.INPUT_FILE)
            with open(input_file_path) as input_file:
                for input_line in input_file:
                    yield input_line.replace("\n", "")

    def part_one(self):
        hexagons = Hexagons.from_line_generator(self.line_generator())
        assert self.part_one_expected_result == hexagons.number_of_black_tiles
        print(f"Part 1 solution: {hexagons.number_of_black_tiles}")

        _final_day_hexagons = hexagons
        for _day in range(1, NUMBER_OF_DAYS + 1):
            _final_day_hexagons = _final_day_hexagons.next_day

            if _day in self.part_two_expected_results:
                if self.part_two_expected_results[_day] != _final_day_hexagons.number_of_black_tiles:
                    raise Exception(
                        f"Day {_day} result did not match expected result: "
                        f"{self.part_two_expected_results[_day]} != "
                        f"{_final_day_hexagons.number_of_black_tiles}"
                    )

        print(f"Part 2 solution: {_final_day_hexagons.number_of_black_tiles}")


def main():
    aoc = AocTwentyFour(test_case=False)
    print(f"Problem 24 took {timeit(aoc.part_one, number=1)} seconds to execute")


if __name__ == "__main__":
    main()
