from typing import Generator, Iterable
from sortedcontainers import SortedList
from collections import OrderedDict, deque
from tqdm import tqdm


Grid = list[list[int]]
Position = tuple[int, int]
Path = OrderedDict[Position, bool]
Frontier = tuple[Path, Position, int]
Direction = tuple[int, int]

UP: Direction = (-1, 0)
DOWN: Direction = (1, 0)
LEFT: Direction = (0, -1)
RIGHT: Direction = (0, 1)

BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
UNDERLINE = "\033[4m"
RESET = "\033[0m"
STRIKETHROUGH = "\033[9m"


def color(style: str, s: str) -> str:
    return f"{style}{s}{RESET}"


def move(position: Position, direction: Direction) -> Position:
    return (position[0] + direction[0], position[1] + direction[1])


def is_valid_position(grid: Grid, position: Position) -> bool:
    return (
        position[0] >= 0
        and position[0] < len(grid)
        and position[1] >= 0
        and position[1] < len(grid[0])
    )


def get_square(grid: Grid, position: Position) -> int:
    return grid[position[0]][position[1]]


def manhattan_distance(p1: Position, p2: Position) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def get_last_n[K, V](
    d: OrderedDict[K, V], n: int
) -> Generator[tuple[K, V], None, None]:
    it = reversed(d.items())
    for _ in range(n):
        n = next(it)
        yield (n[0], n[1])


def window[T](it: Iterable[T], n: int = 2) -> Generator[Iterable[T], None, None]:
    it = iter(it)
    win = deque((next(it, None) for _ in range(n)), maxlen=n)
    yield win
    for e in it:
        win.append(e)
        yield win


def is_straight_line(path: Path, length: int) -> bool:
    if len(path) < length:
        return False

    prev_direction = None
    for (a, _), (b, _) in window(get_last_n(path, length), 2):
        direction = (a[0] - b[0], a[1] - b[1])
        if prev_direction is None:
            prev_direction = direction
        elif prev_direction != direction:
            return False
    return True


def valid_moves(
    grid: Grid, path: Path, position: Position
) -> Generator[Position, None, None]:
    if is_straight_line(path, length=3):
        p, pp = [k for (k, _) in get_last_n(path, 2)]
        direction = (p[0] - pp[0], p[1] - pp[1])
        if direction == UP or direction == DOWN:
            if is_valid_position(grid, move(position, LEFT)):
                yield move(position, LEFT)
            if is_valid_position(grid, move(position, RIGHT)):
                yield move(position, RIGHT)
        elif direction == LEFT or direction == RIGHT:
            if is_valid_position(grid, move(position, UP)):
                yield move(position, UP)
            if is_valid_position(grid, move(position, DOWN)):
                yield move(position, DOWN)
        return

    for direction in [UP, DOWN, LEFT, RIGHT]:
        new_position = move(position, direction)
        if is_valid_position(grid, new_position) and new_position not in path:
            yield new_position


def read_grid(path) -> Grid:
    grid = []
    for line in open(path):
        grid.append([int(c) for c in line.strip()])
    return grid


def print_grid(grid: Grid, position: Position) -> None:
    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            if (i, j) == position:
                print(color(BLUE, "X"), end="")
            else:
                print(col, end="")
        print()


def print_path(grid: Grid, path: Path) -> None:
    pathlist = list(path.keys())
    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            try:
                pi = pathlist.index((i, j))
            except ValueError:
                pi = -1

            if pi >= 0:
                if pi == 0:
                    prev = (0, 0)
                else:
                    prev = pathlist[pi - 1]
                direction = (i - prev[0], j - prev[1])
                if direction == UP:
                    print(color(BLUE, "^"), end="")
                elif direction == DOWN:
                    print(color(BLUE, "v"), end="")
                elif direction == LEFT:
                    print(color(BLUE, "<"), end="")
                elif direction == RIGHT:
                    print(color(BLUE, ">"), end="")
                else:
                    print(color(BLUE, "X"), end="")
            else:
                print(col, end="")
        print()


def score_position(grid: Grid, position: Position) -> int:
    return manhattan_distance(position, (len(grid) - 1, len(grid[0]) - 1))


def score_frontier(grid: Grid, frontier: Frontier) -> int:
    return score_position(grid, frontier[1]) + len(frontier[0])


def rank_moves(grid: Grid, positions: Iterable[Position]) -> list[Position]:
    return sorted(positions, key=lambda p: score_position(grid, p))


def is_valid_path(path: Path) -> bool:
    for (a, _), (b, _) in window(path.items(), 2):
        if manhattan_distance(a, b) > 1:
            return False
    return True


grid: Grid = read_grid("17.smallinput")

frontiers: SortedList[Frontier] = SortedList(
    [(OrderedDict([((0, 0), True)]), (0, 0), 0)], key=lambda f: score_frontier(grid, f)
)

bar = tqdm()
min_loss = 9999999999
while True:
    bar.update(1)
    if len(frontiers) == 0:
        break
    path, position, loss = frontiers.pop(0)
    if loss > min_loss:
        continue
    for new_position in rank_moves(grid, valid_moves(grid, path, position)):
        new_path = path.copy()
        new_path[new_position] = True
        loss += get_square(grid, new_position)
        if new_position == (len(grid) - 1, len(grid[0]) - 1):
            if loss < min_loss:
                min_loss = loss
                print_path(grid, new_path)
                print(loss)
            continue
        frontiers.add((new_path, new_position, loss))
