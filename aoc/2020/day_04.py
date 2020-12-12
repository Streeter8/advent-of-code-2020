import os
from dataclasses import dataclass
from timeit import timeit
from typing import Optional

SAMPLE_INPUT = [
    "ecl:gry pid:860033327 eyr:2020 hcl:#fffffd",
    "byr:1937 iyr:2017 cid:147 hgt:183cm",
    "",
    "iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884",
    "hcl:#cfa07d byr:1929",
    "",
    "hcl:#ae17e1 iyr:2013",
    "eyr:2024",
    "ecl:brn pid:760753108 byr:1931",
    "hgt:179cm",
    "",
    "hcl:#cfa07d eyr:2025 pid:166559648",
    "iyr:2011 ecl:brn hgt:59in",
]

# All 4 are valid in both cases
SAMPLE_INPUT_TWO = [
    "pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980\n",
    "hcl:#623a2f\n",
    "\n",
    "eyr:2029 ecl:blu cid:129 byr:1989\n",
    "iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm\n",
    "\n",
    "hcl:#888785\n",
    "hgt:164cm byr:2001 iyr:2015 cid:88\n",
    "pid:545766238 ecl:hzl\n",
    "eyr:2022\n",
    "\n",
    "iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719\n",
]

HEX_VALUES = set("abcdef0123456789")
EYE_COLORS = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}


@dataclass(frozen=True)
class Passport:
    byr: Optional[str] = None  # (Birth Year)
    iyr: Optional[str] = None  # (Issue Year)
    eyr: Optional[str] = None  # (Expiration Year)
    hgt: Optional[str] = None  # (Height)
    hcl: Optional[str] = None  # (Hair Color)
    ecl: Optional[str] = None  # (Eye Color)
    pid: Optional[str] = None  # (Passport ID)
    cid: Optional[str] = None  # (Country ID)

    @property
    def valid_simple(self) -> bool:
        return bool(
            self.byr
            and self.iyr
            and self.eyr
            and self.hgt
            and self.hcl
            and self.ecl
            and self.pid
        )

    @property
    def valid(self) -> bool:
        return bool(
            self.byr_valid
            and self.iyr_valid
            and self.eyr_valid
            and self.hgt_valid
            and self.hcl_valid
            and self.ecl_valid
            and self.pid_valid
        )

    @property
    def byr_valid(self) -> bool:
        return self.integer_valid(self.byr, 1920, 2002)

    @property
    def iyr_valid(self) -> bool:
        return self.integer_valid(self.iyr, 2010, 2020)

    @property
    def eyr_valid(self) -> bool:
        return self.integer_valid(self.eyr, 2020, 2030)

    @property
    def hgt_valid(self) -> bool:
        if not self.hgt:
            return False

        value = self.hgt[:-2]
        measurement = self.hgt[-2:]
        if measurement == "in":
            return self.integer_valid(value, 59, 76)
        elif measurement == "cm":
            return self.integer_valid(value, 150, 193)
        else:
            return False

    def integer_valid(self, value: str, minimum: int, maximum: int) -> bool:
        try:
            integer_value = int(value)
            return minimum <= integer_value <= maximum
        except Exception:
            return False

    @property
    def hcl_valid(self) -> bool:
        if not self.hcl:
            return False

        if len(self.hcl) != 7:
            return False
        if not self.hcl.startswith("#"):
            return False
        for character in self.hcl[1:]:
            if character not in HEX_VALUES:
                return False

        return True

    @property
    def ecl_valid(self) -> bool:
        return self.ecl in EYE_COLORS

    @property
    def pid_valid(self) -> bool:
        try:
            int(self.pid)
        except Exception:
            return False

        if len(self.pid) != 9:
            return False

        return True


class PassportFactory:
    def __init__(self, passport_args: str):
        self.passport_args = passport_args

    def make(self) -> Passport:
        fields = {}
        for field in self.passport_args.split(" "):
            try:
                field_name, field_value = field.split(":")
            except Exception:
                print(f"{self.passport_args=}; {field=}")
                raise
            fields[field_name] = field_value

        return Passport(**fields)


def input_lines():
    # for line in SAMPLE_INPUT_TWO:
    #     yield line.replace("\n", "")

    directory = os.path.dirname(os.path.abspath(__file__))
    input_file = "day_04.txt"

    input_file_path = os.path.join(directory, "inputs", input_file)
    with open(input_file_path) as input_file:
        for input_line in input_file:
            yield input_line.replace("\n", "")


def passport_args_generator():
    _passport_args = ""
    for input_line in input_lines():
        if not _passport_args:
            _passport_args = input_line
        elif input_line:
            _passport_args = f"{_passport_args} {input_line}"
        else:
            yield _passport_args
            _passport_args = ""

    yield _passport_args


class AocFour:
    def part_one(self):
        """~2ms"""
        valid_passports = 0
        for passport_args in passport_args_generator():
            passport = PassportFactory(passport_args).make()
            if passport.valid_simple:
                valid_passports += 1

        print(f"Part 1 Solution: {valid_passports=}")

    def part_two(self):
        """~3ms"""
        valid_passports = 0
        for passport_args in passport_args_generator():
            passport = PassportFactory(passport_args).make()
            if passport.valid:
                valid_passports += 1

        print(f"Part 2 Solution: {valid_passports=}")


def main():
    aoc = AocFour()
    print(f"Part one took {timeit(aoc.part_one, number=1)} seconds to execute")
    print(f"Part two took {timeit(aoc.part_two, number=1)} seconds to execute")


if __name__ == "__main__":
    main()
