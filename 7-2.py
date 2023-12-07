from collections import defaultdict
from functools import cache

CARDS = list(iter("J23456789TQKA"))


class Hand:
    hand: str
    bid: int

    def __init__(self, hand, bid):
        self.hand = hand
        self.bid = bid

    def __lt__(self, other):
        if self.score() < other.score():
            return True
        elif self.score() > other.score():
            return False

        for a, b in zip(self.hand, other.hand):
            if CARDS.index(a) > CARDS.index(b):
                return False
            elif CARDS.index(a) < CARDS.index(b):
                return True

        return False

    @cache
    def score(self):
        num_jacks = self.hand.count("J")
        hand_without_jacks = self.hand.replace("J", "")

        grouped = defaultdict(int)
        for c in hand_without_jacks:
            grouped[c] += 1

        grouped = list(grouped.values())
        grouped.sort(reverse=True)

        if len(grouped) == 0:
            grouped = [0]
        grouped[0] += num_jacks

        match grouped:
            case [5]:
                return 6
            case [4, 1]:
                return 5
            case [3, 2]:
                return 4
            case [3, 1, 1]:
                return 3
            case [2, 2, 1]:
                return 2
            case [2, 1, 1, 1]:
                return 1
            case [1, 1, 1, 1, 1]:
                return 0

        raise ValueError(f"Invalid hand: {hand}")


hands = []

for line in open("7.input"):
    hand, bid = line.strip().split(" ")
    bid = int(bid)
    hands.append(Hand(hand, bid))

hands.sort()

total = 0
for rank, hand in enumerate(hands, start=1):
    total += hand.bid * rank

print(total)
