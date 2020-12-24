import os
from timeit import timeit

TERMINATOR_DIRECTIONS = {"e", "w"}


class Hexagons:
    def __init__(self, line_generator):
        self.hexagons = {}

        for line in line_generator:
            hexagon = Hexagon(line)

            if self.hexagons.get(hexagon.point, 0):
                self.hexagons[hexagon.point] = 0
            else:
                self.hexagons[hexagon.point] = 1

    @property
    def number_of_black_tiles(self) -> int:
        number_of_black_tiles = 0
        for hexagon in self.hexagons:
            number_of_black_tiles += self.hexagons[hexagon]

        return number_of_black_tiles


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


class AocTwentyFour:
    DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    INPUT_FILE = "day_24.txt"

    def __init__(self):
        pass

    def line_generator(self):
        input_file_path = os.path.join(self.DIRECTORY, "inputs", self.INPUT_FILE)
        with open(input_file_path) as input_file:
            for input_line in input_file:
                yield input_line.replace("\n", "")

        # lines = [
        #     "sesenwnenenewseeswwswswwnenewsewsw\n",
        #     "neeenesenwnwwswnenewnwwsewnenwseswesw\n",
        #     "seswneswswsenwwnwse\n",
        #     "nwnwneseeswswnenewneswwnewseswneseene\n",
        #     "swweswneswnenwsewnwneneseenw\n",
        #     "eesenwseswswnenwswnwnwsewwnwsene\n",
        #     "sewnenenenesenwsewnenwwwse\n",
        #     "wenwwweseeeweswwwnwwe\n",
        #     "wsweesenenewnwwnwsenewsenwwsesesenwne\n",
        #     "neeswseenwwswnwswswnw\n",
        #     "nenwswwsewswnenenewsenwsenwnesesenew\n",
        #     "enewnwewneswsewnwswenweswnenwsenwsw\n",
        #     "sweneswneswneneenwnewenewwneswswnese\n",
        #     "swwesenesewenwneswnwwneseswwne\n",
        #     "enesenwswwswneneswsenwnewswseenwsese\n",
        #     "wnwnesenesenenwwnenwsewesewsesesew\n",
        #     "nenewswnwewswnenesenwnesewesw\n",
        #     "eneswnwswnwsenenwnwnwwseeswneewsenese\n",
        #     "neswnwewnwnwseenwseesewsenwsweewe\n",
        #     "wseweeenwnesenwwwswnew\n",
        # ]
        # for input_line in lines:
        #     yield input_line.replace("\n", "")

    def part_one(self):
        hexagons = Hexagons(self.line_generator())
        print(f"Part 1 solution: {hexagons.number_of_black_tiles}")

    def part_two(self):
        pass


def main():
    aoc = AocTwentyFour()
    print(f"Part one took {timeit(aoc.part_one, number=1)} seconds to execute")
    # print(f"Part two took {timeit(aoc.part_two, number=1)} seconds to execute")


if __name__ == "__main__":
    main()
