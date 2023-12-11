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

empty_y = [i for i, row in enumerate(grid) if all(c == "." for c in row)]
empty_x = [i for i, col in enumerate(zip(*grid)) if all(c == "." for c in col)]
empty_factor = 1_000_000


def find_galaxies(grid: Grid) -> list[Point]:
    galaxies: list[Point] = []

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "#":
                galaxies.append((x, y))

    return galaxies


def modified_manhatten_distance(p1: Point, p2: Point) -> int:
    distance = 0
    for x in range(*sorted([p1[0], p2[0]])):
        if x in empty_x:
            distance += empty_factor
        else:
            distance += 1

    for y in range(*sorted([p1[1], p2[1]])):
        if y in empty_y:
            distance += empty_factor
        else:
            distance += 1

    return distance


galaxies = find_galaxies(grid)

total = 0
for g1, g2 in combinations(galaxies, 2):
    total += modified_manhatten_distance(g1, g2)

print(total)
