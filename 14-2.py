from typing import Literal
from tqdm import tqdm


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


def move_rock_north(grid: Grid, point: tuple[int, int]):
    x, y = point
    while y > 0 and grid[y - 1][x] == ".":
        grid[y - 1][x] = "O"
        grid[y][x] = "."
        y -= 1


def move_rock_east(grid: Grid, point: tuple[int, int]):
    x, y = point
    while x < len(grid[0]) - 1 and grid[y][x + 1] == ".":
        grid[y][x + 1] = "O"
        grid[y][x] = "."
        x += 1


def move_rock_south(grid: Grid, point: tuple[int, int]):
    x, y = point
    while y < len(grid) - 1 and grid[y + 1][x] == ".":
        grid[y + 1][x] = "O"
        grid[y][x] = "."
        y += 1


def move_rock_west(grid: Grid, point: tuple[int, int]):
    x, y = point
    while x > 0 and grid[y][x - 1] == ".":
        grid[y][x - 1] = "O"
        grid[y][x] = "."
        x -= 1


def stone_value(grid: Grid, point: tuple[int, int]) -> int:
    _, y = point
    return len(grid) - y


def tilt_north(grid: Grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == "O":
                move_rock_north(grid, (x, y))


def tilt_west(grid: Grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == "O":
                move_rock_west(grid, (x, y))


def tilt_south(grid: Grid):
    for y in range(len(grid) - 1, -1, -1):
        for x in range(len(grid[0])):
            if grid[y][x] == "O":
                move_rock_south(grid, (x, y))


def tilt_east(grid: Grid):
    for y in range(len(grid)):
        for x in range(len(grid[0]) - 1, -1, -1):
            if grid[y][x] == "O":
                move_rock_east(grid, (x, y))


def spin_cycle(grid: Grid):
    tilt_north(grid)
    tilt_west(grid)
    tilt_south(grid)
    tilt_east(grid)


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


def grid_to_str(grid: Grid) -> str:
    return "\n".join("".join(row) for row in grid)


WEIGHTS = []
UNIQUE_WEIGHTS = set()

for i in tqdm(range(10000)):
    spin_cycle(grid)
    weight = calculate_weight(grid)
    WEIGHTS.append(weight)
    UNIQUE_WEIGHTS.add(weight)

print(UNIQUE_WEIGHTS)


def guess_seq_len(seq, verbose=False):
    seq_len = 1
    initial_item = seq[0]
    butfirst_items = seq[1:]
    if initial_item in butfirst_items:
        first_match_idx = butfirst_items.index(initial_item)
        if verbose:
            print(f'"{initial_item}" was found at index 0 and index {first_match_idx}')
        max_seq_len = min(len(seq) - first_match_idx, first_match_idx)
        for seq_len in range(max_seq_len, 0, -1):
            if seq[:seq_len] == seq[first_match_idx : first_match_idx + seq_len]:
                if verbose:
                    print(
                        f"A sequence length of {seq_len} was found at index {first_match_idx}"
                    )
                break

    return seq_len


guess_seq_len(WEIGHTS, verbose=True)
