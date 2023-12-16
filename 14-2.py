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


def move_rock_north(point: tuple[int, int]):
    x, y = point
    while y > 0 and grid[y - 1][x] == ".":
        grid[y - 1][x] = "O"
        grid[y][x] = "."
        y -= 1


def move_rock_east(point: tuple[int, int]):
    x, y = point
    while x < len(grid[0]) - 1 and grid[y][x + 1] == ".":
        grid[y][x + 1] = "O"
        grid[y][x] = "."
        x += 1


def move_rock_south(point: tuple[int, int]):
    x, y = point
    while y < len(grid) - 1 and grid[y + 1][x] == ".":
        grid[y + 1][x] = "O"
        grid[y][x] = "."
        y += 1


def move_rock_west(point: tuple[int, int]):
    x, y = point
    while x > 0 and grid[y][x - 1] == ".":
        grid[y][x - 1] = "O"
        grid[y][x] = "."
        x -= 1


def stone_value(point: tuple[int, int]) -> int:
    _, y = point
    return len(grid) - y


def tilt_north():
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == "O":
                move_rock_north((x, y))


def tilt_west():
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == "O":
                move_rock_west((x, y))


def tilt_south():
    for y in range(len(grid) - 1, -1, -1):
        for x in range(len(grid[0])):
            if grid[y][x] == "O":
                move_rock_south((x, y))


def tilt_east():
    for y in range(len(grid)):
        for x in range(len(grid[0]) - 1, -1, -1):
            if grid[y][x] == "O":
                move_rock_east((x, y))


def spin_cycle():
    tilt_north()
    tilt_west()
    tilt_south()
    tilt_east()


def calculate_weight() -> int:
    weight = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == "O":
                weight += stone_value((x, y))
    return weight


def print_grid():
    for row in grid:
        print("".join(row))


def grid_to_str() -> str:
    return "".join("".join(row) for row in grid)


def diff_strings(s1: str, s2: str):
    for c1, c2 in zip(s1, s2):
        if c1 != c2:
            print("-", end="")
        else:
            print("+", end="")
    print()


start = 0
cycle = 0

SEEN = {}

print("finding cycle...")
for i in range(0, 1000000):
    spin_cycle()
    s = grid_to_str()
    if s in SEEN:
        start = SEEN[s]
        cycle = i - SEEN[s]
        print(f"cycle found: start {start} period {cycle}")
        break
    SEEN[s] = i

if cycle == 0:
    raise ValueError("No cycle found")

iterations = (1000000000 - start) % cycle

for i in range(iterations - 1):
    spin_cycle()

print(calculate_weight())
