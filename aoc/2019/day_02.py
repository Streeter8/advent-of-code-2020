from copy import deepcopy

OP_CODES_ORIGINAL = [
    1, 0, 0, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 1, 9, 19, 1, 19, 5, 23, 2, 6, 23, 27, 1, 6, 27, 31, 2, 31, 9, 35,
    1, 35, 6, 39, 1, 10, 39, 43, 2, 9, 43, 47, 1, 5, 47, 51, 2, 51, 6, 55, 1, 5, 55, 59, 2, 13, 59, 63, 1, 63, 5, 67, 2,
    67, 13, 71, 1, 71, 9, 75, 1, 75, 6, 79, 2, 79, 6, 83, 1, 83, 5, 87, 2, 87, 9, 91, 2, 9, 91, 95, 1, 5, 95, 99, 2, 99,
    13, 103, 1, 103, 5, 107, 1, 2, 107, 111, 1, 111, 5, 0, 99, 2, 14, 0, 0,
]


class AocTwo:
    OP_CODES = None

    def op_codes_part_one(self):
        self.restore_state()

        operations = {
            1: self.add,
            2: self.multiply,
            99: False,
        }

        position = 0
        operation = operations[self.OP_CODES[0]]

        while operation:
            number_one = self.OP_CODES[self.OP_CODES[position + 1]]
            number_two = self.OP_CODES[self.OP_CODES[position + 2]]
            self.OP_CODES[self.OP_CODES[position + 3]] = operation(number_one, number_two)
            position += 4
            operation = operations[self.OP_CODES[position]]

        final_result = self.OP_CODES[0]
        print(f"Part 1 Solution: {final_result}")

    def op_codes_part_two(self):
        operations = {
            1: self.add,
            2: self.multiply,
            99: False,
        }
        max_val = len(OP_CODES_ORIGINAL) - 1
        possible_solutions = []
        for op_2 in range(max_val):
            for op_1 in range(max_val):
                possible_solutions.append((op_1, op_2))

        for possible_solution in possible_solutions:
            self.set_state(*possible_solution)
            position = 0
            operation = operations[self.OP_CODES[0]]
            while operation:
                number_one = self.OP_CODES[self.OP_CODES[position + 1]]
                number_two = self.OP_CODES[self.OP_CODES[position + 2]]
                self.OP_CODES[self.OP_CODES[position + 3]] = operation(number_one, number_two)
                position += 4
                operation = operations[self.OP_CODES[position]]

            final_result = self.OP_CODES[0]
            if final_result == 19690720:
                response = 100 * possible_solution[0] + possible_solution[1]
                print(f"Part 2 Solution: {response}")
                return

        raise Exception("We're not supposed to get here...")

    def add(self, *args) -> int:
        return sum(args)

    def multiply(self, one: int, two: int) -> int:
        return one * two

    def restore_state(self):
        self.set_state(12, 2)

    def set_state(self, one: int, two: int):
        self.OP_CODES = deepcopy(OP_CODES_ORIGINAL)
        self.OP_CODES[1] = one
        self.OP_CODES[2] = two


def main():
    aoc = AocTwo()
    aoc.op_codes_part_one()
    aoc.op_codes_part_two()


if __name__ == "__main__":
    main()
