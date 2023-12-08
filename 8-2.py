import re
import math

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


def solve(start):
    i = 0
    cur = start
    while True:
        direction = directions[i % len(directions)]
        i += 1
        cur = nodes[cur][direction]
        if cur.endswith("Z"):
            return i


cur = [n for n in nodes.keys() if n.endswith("A")]
solutions = []
for c in cur:
    solutions.append(solve(c))

print(math.lcm(*solutions))
