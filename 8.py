import re

f = open("8.input", "r")

directions = list(map(lambda c: 0 if c == "L" else 1, f.readline().strip()))

f.readline()

nodes = {}

for line in f:
    line = line.strip()
    if line == "":
        break

    cur, left, right, *_ = re.split(r"\W+", line)
    nodes[cur] = (left, right)

i = 0
cur = "AAA"
while True:
    direction = directions[i % len(directions)]
    i += 1
    cur = nodes[cur][direction]

    if cur == "ZZZ":
        print(i)
        break
