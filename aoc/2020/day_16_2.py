import os
from dataclasses import dataclass


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
    DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    TICKET_PARAMS_INPUT_FILE = "day_16_ticket_params.txt"
    TICKETS_INPUT_FILE = "day_16_tickets.txt"

    def __init__(self):
        ticket_params_input_file_path = os.path.join(self.DIRECTORY, "inputs", self.TICKET_PARAMS_INPUT_FILE)
        self.ticket_params = []
        self.ticket_params_map = {}

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
                self.ticket_params_map[param.name] = param

        self.valid_tickets = []
        self._construct_valid_tickets()

    def _construct_valid_tickets(self) -> None:
        tickets_input_file_path = os.path.join(self.DIRECTORY, "inputs", self.TICKETS_INPUT_FILE)
        with open(tickets_input_file_path) as input_file:
            for input_line in input_file:
                self._construct_valid_ticket(input_line)

    def _construct_valid_ticket(self, args: str) -> None:
        valid_ticket = True
        int_args = [int(arg) for arg in args.split(",")]
        for arg in int_args:
            value = int(arg)
            valid = False
            for ticket_param in self.ticket_params:
                if ticket_param.valid_param(value):
                    valid = True
                    break

            if not valid:
                valid_ticket = False
                break

        if valid_ticket:
            self.valid_tickets.append(int_args)

    def determine_field_positions(self):
        possible_positions = {
            ticket_param.name: [4, 5, 8, 9, 12, 13]
            for ticket_param in self.ticket_params
        }

        # Provided
        possible_positions["row"] = [0]
        possible_positions["ticket_class"] = [1]
        possible_positions["seat"] = [2]

        # Determined by "Hand"
        # First Pass of analysis
        possible_positions["route"] = [3]  # The only field where 3 is valid
        possible_positions["train"] = [15]  # The only valid position for train

        # All three shared 11, 14, and 16 as the only valid positions
        # Since these fields "don't matter",
        # we can just assign them one of each and carry on
        possible_positions["arrival_station"] = [11]  # 11, 16
        possible_positions["arrival_platform"] = [14]  # 11, 14, 16
        possible_positions["wagon"] = [16]  # 11, 14, 16

        # With the above fields assigned,
        # departure_date is left with only the 6 position as valid
        possible_positions["departure_date"] = [6]

        # With the departure_date assigned,
        # departure_location is left with only the 18 position as valid
        possible_positions["departure_location"] = [18]

        # With the departure_location assigned,
        # departure_track is left with only the 19 position as valid
        possible_positions["departure_track"] = [19]

        # With the departure_track assigned,
        # departure_time is left with only the 7 position as valid
        possible_positions["departure_time"] = [7]

        # With the departure_time assigned,
        # departure_station is left with only the 17 position as valid
        possible_positions["departure_station"] = [17]

        # With the departure_track assigned,
        # departure_platform is left with only the 10 position as valid
        possible_positions["departure_platform"] = [10]

        # This is our final departure field
        # The rest are unassigned, but are not required by the problem

        for param in possible_positions:
            if len(possible_positions[param]) < 2:
                continue

            parameter = self.ticket_params_map[param]
            invalid_positions = set()
            for position in possible_positions[param]:
                for ticket in self.valid_tickets:
                    if (
                        position in invalid_positions
                        or not parameter.valid_param(ticket[position])
                    ):
                        invalid_positions.add(position)

            for invalid_position in invalid_positions:
                possible_positions[param].remove(invalid_position)

            occurs = {pos: 0 for pos in range(20)}
            for key in possible_positions:
                for position in possible_positions[key]:
                    occurs[position] += 1

        print("Breakpoint here for debugger analysis")


class AocSixteen:
    def __init__(self):
        self.ticket_factory = TicketFactory()

    def part_two(self):
        # self.ticket_factory.determine_field_positions()

        ticket = [149, 73, 71, 107, 113, 151, 223, 67, 163, 53, 173, 167, 109, 79, 191, 233, 83, 227, 229, 157]
        product = (
            ticket[6]  # departure_date
            * ticket[7]  # departure_time
            * ticket[10]  # departure_platform
            * ticket[17]  # departure_station
            * ticket[18]  # departure_location
            * ticket[19]  # departure_track
        )
        print(f"Part 2 Solution: {product}")


def main():
    aoc = AocSixteen()
    aoc.part_two()


if __name__ == "__main__":
    main()
