from itertools import product
from typing import Generator, Iterable
from tqdm import tqdm

path = "12.smallinput"


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


def total_possibilities(record: str) -> int:
    return 2 ** record.count("?")


def unfold(ary: list, n: int) -> list:
    ary = ary + ["?"]
    ary = ary * n
    return ary[:-1]


total = 0
lines = open(path).readlines()
for line in lines:
    line = line.strip()
    record, patterns = line.split(" ")
    record = unfold(list(record), 5)
    patterns = unfold(list(map(int, patterns.split(","))), 5)

    possibilities = total_possibilities(record)
    with tqdm(total=possibilities) as t:
        for p in all_possibilities(record):
            t.update(1)
            if matches_pattern(p, patterns):
                total += 1

print(total)
