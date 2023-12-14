from itertools import product
from typing import Generator, Iterable
from tqdm import tqdm

path = "12.input"


def matches_pattern(record: Iterable[str], patterns: list[int]):
    cur = 0
    i = 0
    for c in record:
        if c == "#":
            cur += 1
        elif c == ".":
            if cur > 0:
                if i == len(patterns) or patterns[i] != cur:
                    return False
                cur = 0
                i += 1

    if cur > 0:
        if i == len(patterns) or patterns[i] != cur:
            return False
        i += 1

    return i == len(patterns)


def all_possibilities(record: str) -> Generator[str, None, None]:
    yield from product(*map(lambda x: [".", "#"] if x == "?" else [x], record))


total = 0
lines = open(path).readlines()
for line in tqdm(lines):
    line = line.strip()
    record, patterns = line.split(" ")
    record = list(record)
    patterns = list(map(int, patterns.split(",")))

    for p in all_possibilities(record):
        if matches_pattern(p, patterns):
            total += 1

print(total)
