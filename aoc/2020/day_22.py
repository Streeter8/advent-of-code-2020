from timeit import timeit
from typing import List, Tuple


class Battle:
    def __init__(self, deck_one: List[int], deck_two: List[int]):
        self.player_one_deck = deck_one
        self.player_two_deck = deck_two

    def battle(self) -> Tuple[List[int], int]:
        player_one_deck = [card for card in self.player_one_deck]
        player_two_deck = [card for card in self.player_two_deck]

        while player_one_deck and player_two_deck:
            self._battle(player_one_deck, player_two_deck)

        winning_deck = player_one_deck or player_two_deck
        return winning_deck, self.calculate_score(winning_deck)

    def _battle(self, player_one_deck: List[int], player_two_deck: List[int]):
        """
        This method utilizes the mutability of Python lists
        """
        player_one_card = player_one_deck.pop(0)
        player_two_card = player_two_deck.pop(0)
        if player_one_card > player_two_card:
            player_one_deck.append(player_one_card)
            player_one_deck.append(player_two_card)
        else:
            player_two_deck.append(player_two_card)
            player_two_deck.append(player_one_card)

    def calculate_score(self, deck: List[int]) -> int:
        _deck = [card for card in deck]
        _deck.reverse()

        total = 0
        for index in range(len(_deck)):
            total += _deck[index] * (index + 1)

        return total


class AocTwentyTwo:

    def __init__(self, test_case: bool = True):
        if test_case:
            self.battle = Battle(
                deck_one=[9, 2, 6, 3, 1],
                deck_two=[5, 8, 4, 7, 10],
            )
            self.part_one_solution = 306
        else:
            self.battle = Battle(
                deck_one=[
                    14, 29, 25, 17, 13, 50, 33, 32, 7, 37, 26, 34, 46, 24, 3, 28, 18, 20, 11, 1, 21, 8, 44, 10, 22
                ],
                deck_two=[
                    5, 38, 27, 15, 45, 40, 43, 30, 35, 9, 48, 12, 16, 47, 42, 4, 2, 31, 41, 39, 23, 19, 36, 49, 6
                ],
            )
            self.part_one_solution = 34324

    def part_one(self):
        """~0.5ms"""
        winning_deck, score = self.battle.battle()
        self.validate_part_one(score)
        print(f"Part one solution: {score}")

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
