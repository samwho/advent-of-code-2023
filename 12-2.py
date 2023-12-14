import re
from typing import Generator

path = "12.input"


def unfold(ary: list, n: int, sep=None) -> list:
    if sep:
        ary = ary + [sep]
    ary = ary * n
    return ary[:-1]


def arrangements(
    input_length: int, pattern: list[int]
) -> Generator[list[tuple[int, int]], None, None]:
    def recurse(index, current, pos):
        if index == len(pattern):
            yield current
            return
        start = pos + 1 if current else 0
        for i in range(
            start, input_length - sum(pattern[index:]) - (len(pattern) - index - 1) + 1
        ):
            next_range = (i, pattern[index])  # Tuple of start position and length
            yield from recurse(index + 1, current + [next_range], i + pattern[index])

    yield from recurse(0, [], 0)


def collapse_dots(s: str) -> str:
    return re.sub(r"\.{2,}", ".", s)


def print_arrangement(input_length, arrangement: list[tuple[int, int]]):
    i = 0
    print("|", end="")
    for start, length in arrangement:
        if start > i:
            print("-" * (start - i), end="")
        print("#" * length, end="")
        i = start + length

    if i < input_length:
        print("-" * (input_length - i), end="")
    print("|")


total = 0
lines = open(path).readlines()
for line in lines:
    line = line.strip()
    record, patterns = line.split(" ")
    record = unfold(list(collapse_dots(record)), 5, "?")
    patterns = unfold(list(map(int, patterns.split(","))), 5)

    local_total = 0
    for arrangement in arrangements(len(record), patterns):
        i = 0
        valid = True
        for start, length in arrangement:
            if start > i:
                for j in range(i, start):
                    if record[j] not in [".", "?"]:
                        valid = False
                        break
                if not valid:
                    break
            i = start
            for j in range(start, start + length):
                if record[j] not in ["#", "?"]:
                    valid = False
                    break
            if not valid:
                break
            i += length
        if not valid:
            continue
        if i < len(record):
            for j in range(i, len(record)):
                if record[j] not in [".", "?"]:
                    valid = False
                    break
        if not valid:
            continue

        total += 1
        local_total += 1
    print(f"{''.join(record)} {patterns} -> {local_total}")


print(total)
