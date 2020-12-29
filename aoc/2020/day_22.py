from timeit import timeit
from typing import List, Tuple


class PlayerOneWins(Exception):
    pass


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


class RecursiveBattle(Battle):
    def __init__(self, deck_one: List[int], deck_two: List[int]):
        super().__init__(deck_one, deck_two)
        self.previous_rounds = set()

    def battle(self) -> Tuple[int, List[int], List[int]]:
        player_one_deck = [card for card in self.player_one_deck]
        player_two_deck = [card for card in self.player_two_deck]

        try:
            while player_one_deck and player_two_deck:
                player_one_wins = self._battle(player_one_deck, player_two_deck)
                self.handle_battle_result(player_one_deck, player_two_deck, player_one_wins)
        except PlayerOneWins:
            return 1, player_one_deck, player_two_deck

        winner = 1 if player_one_deck else 2
        return winner, player_one_deck, player_two_deck

    def _battle(self, player_one_deck: List[int], player_two_deck: List[int]) -> bool:
        round_key = self.round_key(player_one_deck, player_two_deck)
        if round_key in self.previous_rounds:
            raise PlayerOneWins()

        self.previous_rounds.add(round_key)

        player_one_card = player_one_deck[0]
        player_two_card = player_two_deck[0]

        if (
            len(player_one_deck) > player_one_card
            and len(player_two_deck) > player_two_card
        ):
            battle = RecursiveBattle(
                player_one_deck[1:player_one_card + 1],
                player_two_deck[1:player_two_card + 1],
            )
            winner, _player_one_deck, _player_two_deck = battle.battle()
            return 1 == winner
        else:
            return player_one_card > player_two_card

    def round_key(self, player_one_deck: List[int], player_two_deck: List[int]) -> str:
        return f"{self.deck_key(player_one_deck)};{self.deck_key(player_two_deck)}"

    def deck_key(self, deck: List[int]) -> str:
        return ",".join(str(card) for card in deck)

    def handle_battle_result(
        self,
        player_one_deck: List[int],
        player_two_deck: List[int],
        player_one_won_battle: bool
    ):
        """
        This method utilizes the mutability of Python lists
        """
        if player_one_won_battle:
            player_one_deck.append(player_one_deck.pop(0))
            player_one_deck.append(player_two_deck.pop(0))
        else:
            player_two_deck.append(player_two_deck.pop(0))
            player_two_deck.append(player_one_deck.pop(0))


class AocTwentyTwo:

    def __init__(self, test_case: bool = True):
        if test_case:
            deck_one = [9, 2, 6, 3, 1]
            deck_two = [5, 8, 4, 7, 10]
            self.part_one_solution = 306
            self.part_two_solution = 291
            self.part_two_solution_min = self.part_two_solution
            self.part_two_solution_max = self.part_two_solution
        else:
            deck_one = [
                14, 29, 25, 17, 13, 50, 33, 32, 7, 37, 26, 34, 46, 24, 3, 28, 18, 20, 11, 1, 21, 8, 44, 10, 22
            ]
            deck_two = [
                5, 38, 27, 15, 45, 40, 43, 30, 35, 9, 48, 12, 16, 47, 42, 4, 2, 31, 41, 39, 23, 19, 36, 49, 6
            ]
            self.part_one_solution = 34324
            self.part_two_solution = 33259
            self.part_two_solution_min = 31970 + 1
            self.part_two_solution_max = 35232 - 1

        self.battle = Battle(deck_one, deck_two)
        self.recursive_battle = RecursiveBattle(deck_one, deck_two)

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

    def part_two(self):
        """"""
        winner, player_one_deck, player_two_deck = self.recursive_battle.battle()
        winning_deck = player_one_deck if 1 == winner else player_two_deck
        score = self.recursive_battle.calculate_score(winning_deck)
        self.validate_part_two(score)
        print(f"Part two solution: {score}")

    def validate_part_two(self, score: int):
        if self.part_two_solution and (score != self.part_two_solution):
            raise Exception(
                f"Score did not match expected result: "
                f"{score} != {self.part_two_solution}"
            )
        elif score < self.part_two_solution_min:
            raise Exception(
                f"Score too low: "
                f"{score} < {self.part_two_solution_min}"
            )
        elif score > self.part_two_solution_max:
            raise Exception(
                f"Score too high: "
                f"{score} > {self.part_two_solution_max}"
            )


def main():
    aoc = AocTwentyTwo(test_case=False)
    print(f"Part one took {timeit(aoc.part_one, number=1)} seconds to execute")
    print(f"Part two took {timeit(aoc.part_two, number=1)} seconds to execute")


if __name__ == "__main__":
    main()
