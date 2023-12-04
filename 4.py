import re

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

    score = 0
    for n in ours:
        if n in winning:
            if score == 0:
                score += 1
            else:
                score *= 2
    total += score
print(total) 
