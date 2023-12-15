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


def find_identical_pairs[T](
    it: Iterable[T], tolerance: int = 0
) -> Generator[tuple[int, int, int], None, None]:
    for (i, a), (j, b) in window(enumerate(it), 2):
        diff = sum(c != d for (c, d) in zip(a, b))
        if diff <= tolerance:
            yield (i, j, diff)


def print_grid(grid: Grid):
    for row in grid:
        print("".join(row))


def is_horizontal_mirror(grid: Grid, line: tuple[int, int], tolerance: int = 0) -> bool:
    a, b = line
    while a >= 0 and b < len(grid):
        diff = sum(c != d for (c, d) in zip(get_row(grid, a), get_row(grid, b)))
        tolerance -= diff
        if tolerance < 0:
            return False
        a -= 1
        b += 1
    return tolerance == 0


def is_vertical_mirror(grid: Grid, line: tuple[int, int], tolerance: int = 0) -> bool:
    a, b = line
    while a >= 0 and b < len(grid[0]):
        diff = sum(c != d for (c, d) in zip(get_col(grid, a), get_col(grid, b)))
        tolerance -= diff
        if tolerance < 0:
            return False
        a -= 1
        b += 1
    return tolerance == 0


path = "13.input"
f = open(path, "r")

horizontal_total = 0
vertical_total = 0

while grid := read_grid(f):
    for a, b in window(iter(range(len(grid))), 2):
        if is_horizontal_mirror(grid, (a, b), tolerance=1):
            horizontal_total += a + 1
            break

    for a, b in window(iter(range(len(grid[0]))), 2):
        if is_vertical_mirror(grid, (a, b), tolerance=1):
            vertical_total += a + 1
            break

print(vertical_total + 100 * horizontal_total)
