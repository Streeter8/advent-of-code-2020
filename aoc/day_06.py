import os
import sys

class Orbit:
    def __init__(self, input: str):
        inputs = input.split(")")
        self.planet = inputs[0]
        self.moon = inputs[1]


class Planet:
    def __init__(self, name: str):
        self.name = name
        self.moons = []

    def number_of_orbits(self, level: int = 0) -> int:
        return level + sum(moon.number_of_orbits(level + 1) for moon in self.moons)

    def add_moon(self, moon):
        self.moons.append(moon)


class AocOrbits:
    """
    Template file for solutions
    """
    DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    INPUT_FILE = "day_06.txt"
    orbits = {}

    def part_one(self):
        input_file_path = os.path.join(self.DIRECTORY, "inputs", self.INPUT_FILE)

        with open(input_file_path) as input_file:
            for input_line in input_file:
                orbit = Orbit(input_line.replace("\n", ""))
                if orbit.planet in self.orbits:
                    self.orbits[orbit.planet].append(orbit.moon)
                else:
                    self.orbits[orbit.planet] = [orbit.moon]

        center_of_mass = Planet("COM")
        self.process_moons(center_of_mass)
        print(f"The total number of direct and indirect orbits: {center_of_mass.number_of_orbits()}")
        # Answer: 186597

    def process_moons(self, planet: Planet):
        if planet.name in self.orbits:
            for moon in self.orbits[planet.name]:
                new_moon = Planet(moon)
                self.process_moons(new_moon)
                planet.add_moon(new_moon)

    def part_two(self):
        total = "Not Implemented"
        print(f"Part 2 Solution: {total}")


def main():
    """
    The default recursion limit is 1000 levels.
    We need just a little more to be able to process the provided data.
    I don't feel so bad for bumping the limit since it's only a few more levels.
    """
    sys.setrecursionlimit(1075)
    aoc = AocOrbits()
    aoc.part_one()
    # aoc.part_two()


if __name__ == "__main__":
    main()
