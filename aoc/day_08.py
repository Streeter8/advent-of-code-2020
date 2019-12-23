import os


class Row:
    def __init__(self, row_input: str):
        self.input = [character for character in row_input]
        characters = {character for character in row_input}
        self.characters = {
            character: row_input.count(character)
            for character in characters
        }


class Layer:
    def __init__(self, width, layer_input):
        self.rows = []
        self.characters = {}
        for index in range(0, len(layer_input), width):
            row = Row(layer_input[index: index + width])
            self.rows.append(row)
            for character in row.characters:
                if character not in self.characters:
                    self.characters[character] = row.characters[character]
                else:
                    self.characters[character] = self.characters[character] + row.characters[character]

    def get_pixel(self, x: int, y: int) -> str:
        return self.rows[y].input[x]

    def _chars(self, char: str) -> int:
        return self.characters.get(char, 0)

    @property
    def zeroes(self) -> int:
        return self._chars("0")

    @property
    def ones(self) -> int:
        return self._chars("1")

    @property
    def twos(self) -> int:
        return self._chars("2")


class SecretImage:
    def __init__(self, width, height, file_input):
        self.width = width
        self.height = height
        layer_length = width * height
        self.layers = [
            Layer(width, file_input[index: index + layer_length])
            for index in range(0, len(file_input), layer_length)
        ]

    def translate_image(self) -> str:
        image_string = ""
        for y_index in range(0, self.height):
            for x_index in range(0, self.width):
                image_string = f"{image_string}{self.get_pixel(x_index, y_index)}"
            image_string = f"{image_string}\n"
        return image_string

    def get_pixel(self, x: int, y: int) -> str:
        for index in range(0, len(self.layers)):
            pixel = self.layers[index].get_pixel(x, y)
            if pixel == "1":
                return "X"
            if pixel == "0":
                return " "
        return " "


class Aoc:
    """
    Template file for solutions
    """
    DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    INPUT_FILE = "day_08.txt"
    WIDTH = 25
    HEIGHT = 6

    def run(self):
        input_file_path = os.path.join(self.DIRECTORY, "inputs", self.INPUT_FILE)
        file_input = None

        with open(input_file_path) as input_file:
            for input_line in input_file:
                file_input = input_line.replace("\n", "")

        secret_image = SecretImage(self.WIDTH, self.HEIGHT, file_input)

        lowest_layer = None
        for layer in secret_image.layers:
            if lowest_layer:
                if lowest_layer.zeroes > layer.zeroes:
                    lowest_layer = layer
            else:
                lowest_layer = layer

        print(f"Part 1 Solution: {lowest_layer.ones * lowest_layer.twos}")
        # Result: 2048

        result = secret_image.translate_image()
        print(f"Part 2 Solution:\n{result}")
        # Result: HFYAK


def main():
    aoc = Aoc()
    aoc.run()


if __name__ == "__main__":
    main()
