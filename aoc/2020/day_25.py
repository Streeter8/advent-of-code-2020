from timeit import timeit


class Factory:
    LOOP_KEY = 20201227

    def __init__(self, subject_number: int):
        self.subject_number = subject_number

    def make(self) -> int:
        raise NotImplementedError

    def _iterate(self, value: int) -> int:
        return (value * self.subject_number) % self.LOOP_KEY


class LoopSizeFactory(Factory):
    def __init__(self, subject_number: int, public_key: int):
        super().__init__(subject_number)

        self.public_key = public_key

    def make(self) -> int:
        value = 1
        loop_size = 0

        while value != self.public_key:
            value = self._iterate(value)
            loop_size += 1

        return loop_size


class KeyFactory(Factory):
    def __init__(self, subject_number: int, loop_size: int):
        super().__init__(subject_number)

        self.loop_size = loop_size

    def make(self) -> int:
        value = 1

        for _ in range(self.loop_size):
            value = self._iterate(value)

        return value


class AocTwentyFive:

    def __init__(self, test_case: bool = True):
        if test_case:
            self.card_public_key = 5764801
            self.door_public_key = 17807724
        else:
            self.card_public_key = 18499292
            self.door_public_key = 8790390

    def part_one(self):
        """~4.5 seconds"""
        card_loop_size = LoopSizeFactory(subject_number=7, public_key=self.card_public_key).make()
        door_by_card_encryption_key = KeyFactory(self.door_public_key, card_loop_size).make()

        print(f"Part one solution: {door_by_card_encryption_key}")

        # door_loop_size = LoopSizeFactory(subject_number=7, public_key=self.door_public_key).make()
        # card_by_door_encryption_key = KeyFactory(self.card_public_key, door_loop_size).make()

    def part_two(self):
        pass


def main():
    aoc = AocTwentyFive(test_case=False)
    print(f"Part one took {timeit(aoc.part_one, number=1)} seconds to execute")
    # print(f"Part two took {timeit(aoc.part_two, number=1)} seconds to execute")


if __name__ == "__main__":
    main()
