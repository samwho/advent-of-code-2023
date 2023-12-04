from functools import cache
import re

class ScratchCard:
    def __init__(self, original, number, winning, ours):
        self.original = original
        self.number = number
        self.winning = set(winning)
        self.ours = set(ours)

    @cache
    def score(self):
        score = 0
        for n in self.ours:
            if n in self.winning:
                score += 1
        return score

    def __str__(self):
        w = ', '.join([str(n) for n in self.winning])
        o = ', '.join([str(n) for n in self.ours])
        return f'{self.number}: {w} | {o} ({self.score()})'

cards = {}
todo = []
totals = {}

total = 0
for line in open('4.input'):
    line = line.strip()
    preamble, rest = line.split(': ')
    _, number = re.split('\s+', preamble)
    number = int(number)

    winning, ours = rest.split(' | ')
    winning = winning.strip()
    ours = ours.strip()

    winning = [int(n) for n in re.split('\s+', winning)]
    ours = [int(n) for n in re.split('\s+', ours)]

    cards[number] = ScratchCard(line, number, winning, ours)
    todo.append(cards[number])
    totals[number] = 1

n = 0
while len(todo) > 0:
    n += 1
    if n % 10000 == 0:
        print(f'{n} {len(todo)}')
    card = todo.pop()
    score = card.score()
    for i in range(card.number + 1, card.number + score + 1):
        todo.append(cards[i])
        totals[card.number] += 1

total = 0
for n in totals.values():
    total += n
print(total)
