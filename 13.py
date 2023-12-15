from typing import Literal, Generator, Iterable
from io import TextIOWrapper
from collections import deque


Square = Literal[".", "#"]
Grid = list[list[Square]]


def read_grid(f: TextIOWrapper) -> Grid | None:
    grid = []
    while line := f.readline().strip():
        grid.append(list(line.strip()))
    if grid == []:
        return None
    return grid


def get_row(grid: Grid, row: int) -> list[Square]:
    return grid[row]


def get_col(grid: Grid, col: int) -> list[Square]:
    return [row[col] for row in grid]


def rows(grid: Grid) -> Generator[list[Square], None, None]:
    yield from grid


def cols(grid: Grid) -> Generator[list[Square], None, None]:
    return (get_col(grid, col) for col in range(len(grid[0])))


def window[T](it: Iterable[T], n: int = 2) -> Generator[Iterable[T], None, None]:
    win = deque((next(it, None) for _ in range(n)), maxlen=n)
    yield win
    for e in it:
        win.append(e)
        yield win


def find_identical_pairs[T](it: Iterable[T]) -> Generator[tuple[int, int], None, None]:
    for (i, a), (j, b) in window(enumerate(it), 2):
        if a == b:
            yield (i, j)


def print_grid(grid: Grid):
    for row in grid:
        print("".join(row))


path = "13.input"
f = open(path, "r")

horizontal_total = 0
vertical_total = 0

while grid := read_grid(f):
    for a, b in find_identical_pairs(rows(grid)):
        mirror = True
        oga, ogb = a, b
        size = a + 1
        while a >= 0 and b < len(grid):
            if get_row(grid, a) != get_row(grid, b):
                mirror = False
                break
            a -= 1
            b += 1

        if mirror:
            horizontal_total += size
            break

    for a, b in find_identical_pairs(cols(grid)):
        mirror = True
        oga, ogb = a, b
        size = a + 1
        while a >= 0 and b < len(grid[0]):
            if get_col(grid, a) != get_col(grid, b):
                mirror = False
                break
            a -= 1
            b += 1

        if mirror:
            vertical_total += size
            break

print(vertical_total + 100 * horizontal_total)
