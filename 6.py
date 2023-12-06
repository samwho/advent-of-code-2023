import re
from typing import Iterator

def distance(hold: int, duration: int) -> int:
    return hold * (duration - hold)

def distances(duration: int) -> Iterator[int]:
    return map(lambda h: distance(h, duration), range(duration))

f = open("6.input", "r")

times = list(map(int, (filter(lambda f: f, re.split(r"\s+", f.readline().split(":")[1])))))
records = list(map(int, (filter(lambda f: f, re.split(r"\s+", f.readline().split(":")[1])))))

total = 1
for time, record in zip(times, records):
    total *= len(list(filter(lambda d: d > record, distances(time))))

print(total)

