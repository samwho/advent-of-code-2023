from itertools import combinations
from typing import Literal

Point = tuple[int, int]
Square = Literal["#", "."]
Grid = list[list[Square]]

path = "11.input"
grid: Grid = list(
    map(
        lambda line: list(iter(line.strip())),
        open(path, "r").read().strip().split("\n"),
    )
)


def expand_universe(grid: Grid) -> Grid:
    grid = grid.copy()

    i = 0
    while True:
        if i == len(grid):
            break

        if all((c == "." for c in grid[i])):
            grid.insert(i, ["."] * len(grid[i]))
            i += 1

        i += 1

    i = 0
    while True:
        if i == len(grid[0]):
            break

        if all((grid[j][i] == "." for j in range(len(grid)))):
            for j in range(len(grid)):
                grid[j].insert(i, ".")
            i += 1

        i += 1

    return grid


def find_galaxies(grid: Grid) -> list[Point]:
    galaxies: list[Point] = []

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "#":
                galaxies.append((x, y))

    return galaxies


def manhatten_distance(p1: Point, p2: Point) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


grid = expand_universe(grid)
galaxies = find_galaxies(grid)

total = 0
for g1, g2 in combinations(galaxies, 2):
    total += manhatten_distance(g1, g2)

print(total)
