import os
from dataclasses import dataclass
from timeit import timeit

DIRECTORY = os.path.dirname(os.path.abspath(__file__))


@dataclass(frozen=True)
class TicketParam:
    name: int
    lower_min: int
    lower_max: int
    upper_min: int
    upper_max: int

    def valid_param(self, param: int) -> bool:
        return (
            self.lower_min <= param <= self.lower_max
            or self.upper_min <= param <= self.upper_max
        )


class TicketFactory:
    TICKET_PARAMS_INPUT_FILE = "day_16_ticket_params.txt"

    def __init__(self):
        ticket_params_input_file_path = os.path.join(DIRECTORY, "inputs", self.TICKET_PARAMS_INPUT_FILE)
        self.ticket_params = []

        with open(ticket_params_input_file_path) as input_file:
            for input_line in input_file:
                attribute_name, args = input_line.split(":")
                name = attribute_name.replace(" ", "_")
                if name == "class":
                    name = "ticket_class"

                boundary_args = args.replace(" ", "")
                lower, upper = boundary_args.split("or")
                lower_min, lower_max = lower.split("-")
                upper_min, upper_max = upper.split("-")

                param = TicketParam(name, int(lower_min), int(lower_max), int(upper_min), int(upper_max))
                self.ticket_params.append(param)

    def get_error_rate(self, args: str) -> int:
        error_rate = 0

        for arg in args.split(","):
            value = int(arg)
            valid = False
            for ticket_param in self.ticket_params:
                if ticket_param.valid_param(value):
                    valid = True

            if not valid:
                error_rate += value

        return error_rate


class AocSixteen:
    DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    TICKETS_INPUT_FILE = "day_16_tickets.txt"

    def __init__(self):
        self.ticket_factory = TicketFactory()

    def part_one(self):
        error_rate = 0
        tickets_input_file_path = os.path.join(DIRECTORY, "inputs", self.TICKETS_INPUT_FILE)
        with open(tickets_input_file_path) as input_file:
            for input_line in input_file:
                error_rate += self.ticket_factory.get_error_rate(input_line)

        print(f"Part 1 Solution: {error_rate=}")


def main():
    aoc = AocSixteen()
    print(f"Part one took {timeit(aoc.part_one, number=1)} seconds to execute")


if __name__ == "__main__":
    main()
