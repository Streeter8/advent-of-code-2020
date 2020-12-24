from timeit import timeit


class AocTwentyTwo:

    def __init__(self, test_case: bool = True):
        if test_case:
            self.player_one_deck = [9, 2, 6, 3, 1]
            self.player_two_deck = [5, 8, 4, 7, 10]
            self.part_one_solution = 306
        else:
            self.player_one_deck = [
                14, 29, 25, 17, 13, 50, 33, 32, 7, 37, 26, 34, 46, 24, 3, 28, 18, 20, 11, 1, 21, 8, 44, 10, 22
            ]
            self.player_two_deck = [
                5, 38, 27, 15, 45, 40, 43, 30, 35, 9, 48, 12, 16, 47, 42, 4, 2, 31, 41, 39, 23, 19, 36, 49, 6
            ]
            self.part_one_solution = None

    def part_one(self):
        """~0.5ms"""
        self.battle()

        score = self.calculate_score()
        print(f"Part one solution: {score}")

    def battle(self):
        while self.player_one_deck and self.player_two_deck:
            player_one_card = self.player_one_deck.pop(0)
            player_two_card = self.player_two_deck.pop(0)
            if player_one_card > player_two_card:
                self.player_one_deck.append(player_one_card)
                self.player_one_deck.append(player_two_card)
            else:
                self.player_two_deck.append(player_two_card)
                self.player_two_deck.append(player_one_card)

    def calculate_score(self) -> int:
        deck = self.player_one_deck if self.player_one_deck else self.player_two_deck
        deck.reverse()

        total = 0
        for index in range(len(deck)):
            total += deck[index] * (index + 1)

        return total

    def validate_part_one(self, score: int):
        if self.part_one_solution and (score != self.part_one_solution):
            raise Exception(
                f"Score did not match expected result: "
                f"{score} != {self.part_one_solution}"
            )


def main():
    aoc = AocTwentyTwo(test_case=False)
    print(f"Part one took {timeit(aoc.part_one, number=1)} seconds to execute")


if __name__ == "__main__":
    main()
