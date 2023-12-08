import re
import math
import itertools

f = open("8.input","r")

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
cur = [n for n in nodes.keys() if n.endswith("A")]
factors = [[] for _ in cur]

while True:
    for j in range(len(cur)):
        direction = directions[i % len(directions)]
        i += 1
        cur[j] = nodes[cur[j]][direction]
        if cur[j].endswith("Z"):
            factors[j].append(i)
    
    if all([len(f) > 20 for f in factors]):
        break

smallest = 0
for p in itertools.product(*factors):
    lcm = math.lcm(*p)
    if smallest == 0 or lcm < smallest:
        smallest = lcm

print(smallest)

# 2527019372856
# 881518385880
# 92791409040