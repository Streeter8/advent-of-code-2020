import os
import sys


class Orbit:
    def __init__(self, input: str):
        inputs = input.split(")")
        self.planet = inputs[0]
        self.moon = inputs[1]


class Planet:
    def __init__(self, name: str, parent_planet):
        self.name = name
        self.parent_planet = parent_planet
        self.moons = []

    def number_of_orbits(self, level: int = 0) -> int:
        return level + sum(moon.number_of_orbits(level + 1) for moon in self.moons)

    def add_moon(self, moon):
        self.moons.append(moon)

    @property
    def planet_path(self):
        if self.parent_planet:
            parent_path = self.parent_planet.planet_path
            parent_path.append(self.name)
            return parent_path
        else:
            return [self.name]


class AocOrbits:
    """
    Template file for solutions
    """
    DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    INPUT_FILE = "day_06.txt"
    INPUT_FILE_PART_TWO = "day_06_part_two.txt"
    orbits = {}
    center_of_mass = None
    you_planet = None
    santa_planet = None

    def reset(self):
        self.orbits = {}
        self.center_of_mass = None
        self.you_planet = None
        self.santa_planet = None

    def part_one(self):
        input_file_path = os.path.join(self.DIRECTORY, "inputs", self.INPUT_FILE)

        with open(input_file_path) as input_file:
            for input_line in input_file:
                orbit = Orbit(input_line.replace("\n", ""))
                if orbit.planet in self.orbits:
                    self.orbits[orbit.planet].append(orbit.moon)
                else:
                    self.orbits[orbit.planet] = [orbit.moon]

        center_of_mass = Planet("COM", None)
        self.process_moons(center_of_mass)
        self.center_of_mass = center_of_mass

        print(f"The total number of direct and indirect orbits: {self.center_of_mass.number_of_orbits()}")
        # Result: 186597

    def part_two(self):
        input_file_path = os.path.join(self.DIRECTORY, "inputs", self.INPUT_FILE_PART_TWO)

        with open(input_file_path) as input_file:
            for input_line in input_file:
                orbit = Orbit(input_line.replace("\n", ""))
                if orbit.planet in self.orbits:
                    self.orbits[orbit.planet].append(orbit.moon)
                else:
                    self.orbits[orbit.planet] = [orbit.moon]

        center_of_mass = Planet("COM", None)
        self.process_moons(center_of_mass)
        self.center_of_mass = center_of_mass

        you_path = self.you_planet.planet_path
        santa_path = self.santa_planet.planet_path
        diff = (set(you_path).symmetric_difference(set(santa_path))).difference({"SAN", "YOU"})

        print(f"Minimal number of orbital jumps required: {len(diff)}")
        # Result: 412

    def process_moons(self, planet: Planet):
        if planet.name in self.orbits:
            for moon in self.orbits[planet.name]:
                new_moon = Planet(name=moon, parent_planet=planet)
                self.process_moons(new_moon)
                planet.add_moon(new_moon)
                if new_moon.name == "YOU":
                    self.you_planet = new_moon
                if new_moon.name == "SAN":
                    self.santa_planet = new_moon


def main():
    """
    The default recursion limit is 1000 levels.
    We need just a little more to be able to process the provided data.
    I don't feel so bad for bumping the limit since it's only a few more levels.
    """
    sys.setrecursionlimit(1075)
    aoc = AocOrbits()
    aoc.part_one()
    aoc.reset()
    aoc.part_two()


if __name__ == "__main__":
    main()
