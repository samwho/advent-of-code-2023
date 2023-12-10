from typing import Literal

DEBUG = False


def debug(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


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


Square = Literal["L", "|", "J", "7", "F", "-", ".", "S"]
Point = tuple[int, int]
Direction = tuple[int, int]
Grid = list[list[Square]]

UP: Direction = (0, -1)
DOWN: Direction = (0, 1)
LEFT: Direction = (-1, 0)
RIGHT: Direction = (1, 0)

HAS_RIGHT: list[Square] = ["S", "L", "-", "F"]
HAS_LEFT: list[Square] = ["S", "7", "-", "J"]
HAS_UP: list[Square] = ["S", "L", "|", "J"]
HAS_DOWN: list[Square] = ["S", "7", "|", "F"]


def to_unicode(s: Square) -> str:
    if s == "L":
        return "╰"
    elif s == "J":
        return "╯"
    elif s == "7":
        return "╮"
    elif s == "F":
        return "╭"
    elif s == "|":
        return "│"
    elif s == "-":
        return "─"
    elif s == "S":
        return "S"
    raise ValueError(f"Unknown square {s}")


file = "10.input"

grid: Grid = list(
    map(
        lambda line: list(iter(line.strip())),
        open(file).read().splitlines(),
    )
)

path: list[Point] = []
for line in open(f"{file}.path", "r"):
    x, y = map(int, line.strip().split(" "))
    path.append((x, y))

path_dict = {(p[0], p[1]): True for p in path}
inside = 0


def is_inside_path(point: Point) -> bool:
    val = grid[point[1]][point[0]]

    intersects = ["J", "L", "|"]
    total = 0

    line = []
    orig = point

    while point[0] >= 0:
        line.append(point)
        val = grid[point[1]][point[0]]
        if val == "S":
            val = "J"
        if point in path_dict and val in intersects:
            total += 1
        point = (point[0] - 1, point[1])

    if DEBUG:
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                val = grid[y][x]
                if (x, y) == orig:
                    debug(color(GREEN, "X"), end="")
                elif (x, y) in line and (x, y) in path_dict:
                    if val in intersects:
                        debug(color(STRIKETHROUGH, color(RED, to_unicode(val))), end="")
                    else:
                        debug(color(STRIKETHROUGH, to_unicode(val)), end="")
                elif (x, y) in line:
                    debug(color(STRIKETHROUGH, " "), end="")
                elif (x, y) in path_dict:
                    debug(to_unicode(val), end="")
                else:
                    debug(" ", end="")
            debug()
        debug(f"{'inside' if total % 2 == 1 else 'outside'} -> {total}")

    return total % 2 == 1


for y in range(len(grid)):
    for x in range(len(grid[y])):
        if (x, y) in path_dict:
            continue
        if is_inside_path((x, y)):
            inside += 1

print(inside)
