from typing import Literal


RoundRock = Literal["O"]
CubeRock = Literal["#"]
Space = Literal["."]
Square = RoundRock | CubeRock | Space
Grid = list[list[Square]]

path = "14.input"
f = open(path, "r")

grid: Grid = []
for line in f:
    grid.append(list(line.strip()))


def move_rock_north(grid: Grid, point: tuple[int, int]) -> Grid:
    x, y = point
    while y > 0 and grid[y - 1][x] == ".":
        grid[y - 1][x] = "O"
        grid[y][x] = "."
        y -= 1


def stone_value(grid: Grid, point: tuple[int, int]) -> int:
    x, y = point
    return len(grid) - y


def tilt_north(grid: Grid) -> Grid:
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == "O":
                move_rock_north(grid, (x, y))


def calculate_weight(grid: Grid) -> int:
    weight = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == "O":
                weight += stone_value(grid, (x, y))
    return weight


def print_grid(grid: Grid):
    for row in grid:
        print("".join(row))


tilt_north(grid)
print(calculate_weight(grid))
