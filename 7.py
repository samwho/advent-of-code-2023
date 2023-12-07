from collections import defaultdict

CARDS = list(iter("23456789TJQKA"))


class Hand:
    hand: str
    bid: int

    def __init__(self, hand, bid):
        self.hand = hand
        self.bid = bid

    def __lt__(self, other):
        return cmp_hands(self.hand, other.hand) < 0


def score(hand):
    grouped = defaultdict(int)
    for c in hand:
        grouped[c] += 1

    grouped = list(grouped.values())
    grouped.sort(reverse=True)
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


def cmp_hands(hand1, hand2):
    score1 = score(hand1)
    score2 = score(hand2)

    if score1 > score2:
        return 1
    elif score1 < score2:
        return -1

    for a, b in zip(hand1, hand2):
        if CARDS.index(a[0]) > CARDS.index(b[0]):
            return 1
        elif CARDS.index(a[0]) < CARDS.index(b[0]):
            return -1

    return 0


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
