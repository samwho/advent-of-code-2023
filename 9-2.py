def window(seq, size):
    for i in range(len(seq) - size + 1):
        yield seq[i : i + size]


def next_in_sequence(sequence: list[int]) -> int:
    derivatives = []

    d = 0
    c = sequence
    while True:
        derivatives.append([b - a for a, b in window(c, 2)])
        if all([n == 0 for n in derivatives[d]]):
            break
        c = derivatives[d]
        d += 1

    while d > 0:
        d -= 1
        derivatives[d].append(derivatives[d][-1] + derivatives[d + 1][-1])

    return sequence[-1] + derivatives[0][-1]


total = 0
for line in open("9.input"):
    nums = list(map(int, reversed(line.strip().split(" "))))
    answer = next_in_sequence(nums)
    total += answer
print(total)
