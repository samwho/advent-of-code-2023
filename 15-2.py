import re


def hash(s: str) -> int:
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h = h % 256
    return h


BUCKETS = [[] for _ in range(256)]

path = "15.input"
input = open(path).read().strip()

for command in input.split(","):
    result = re.split(r"(\w+)([=-])(\d)?", command)
    label, op, power = result[1], result[2], result[3]

    if op == "=":
        b = BUCKETS[hash(label)]
        for i, (l, p) in enumerate(b):
            if l == label:
                b[i] = (l, int(power))
                break
        else:
            b.append((label, int(power)))
    elif op == "-":
        b = BUCKETS[hash(label)]
        for i, (l, p) in enumerate(b):
            if l == label:
                b.pop(i)
                break

total = 0
for i, b in enumerate(BUCKETS):
    for j, (_, p) in enumerate(b):
        total += (i + 1) * (j + 1) * p
print(total)
