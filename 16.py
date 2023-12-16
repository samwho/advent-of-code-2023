from typing import Literal

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


Space = Literal["."]
Mirror = Literal["/", "\\"]
Splitter = Literal["|", "-"]
Square = Space | Mirror | Splitter
Grid = list[list[Square]]
Position = tuple[int, int]
Direction = tuple[-1 | 0 | 1, -1 | 0 | 1]
Beam = tuple[Position, Direction]

UP: Direction = (-1, 0)
DOWN: Direction = (1, 0)
LEFT: Direction = (0, -1)
RIGHT: Direction = (0, 1)


def read_grid(path) -> Grid:
    return [list(line.strip()) for line in open(path)]


def print_grid(grid: Grid, energised: set[Position], beams: list[Beam]):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            glyph = grid[y][x]
            c = WHITE
            if (y, x) in energised:
                c = GREEN
            beam = [beam for beam in beams if beam[0] == (y, x)]
            if len(beam) > 0:
                if beam[0][1] == UP:
                    glyph = "^"
                elif beam[0][1] == DOWN:
                    glyph = "v"
                elif beam[0][1] == LEFT:
                    glyph = "<"
                elif beam[0][1] == RIGHT:
                    glyph = ">"
            print(color(c, glyph), end="")
        print()


def move(position: Position, direction: Direction) -> Position:
    return (position[0] + direction[0], position[1] + direction[1])


def is_in_bounds(grid: Grid, position: Position) -> bool:
    return 0 <= position[0] < len(grid) and 0 <= position[1] < len(grid[0])


def get_square(grid: Grid, position: Position) -> Square:
    return grid[position[0]][position[1]]


grid = read_grid("16.input")

BEAMS: list[Beam] = [((0, -1), RIGHT)]
ENERGISED: set[Position] = set([(0, 0)])
SEEN: set[Beam] = set()

while True:
    # print(len(BEAMS))
    # print_grid(grid, ENERGISED, BEAMS)
    # input()
    if len(BEAMS) == 0:
        break

    position, direction = BEAMS.pop()
    position = move(position, direction)
    if (position, direction) in SEEN:
        continue
    SEEN.add((position, direction))
    if not is_in_bounds(grid, position):
        continue

    ENERGISED.add(position)

    square = get_square(grid, position)

    if square == ".":
        BEAMS.append((position, direction))
    elif square == "|":
        if direction in [UP, DOWN]:
            BEAMS.append((position, direction))
        else:
            BEAMS.append((position, UP))
            BEAMS.append((position, DOWN))
    elif square == "-":
        if direction in [LEFT, RIGHT]:
            BEAMS.append((position, direction))
        else:
            BEAMS.append((position, LEFT))
            BEAMS.append((position, RIGHT))
    elif square == "/":
        if direction == UP:
            BEAMS.append((position, RIGHT))
        elif direction == RIGHT:
            BEAMS.append((position, UP))
        elif direction == DOWN:
            BEAMS.append((position, LEFT))
        elif direction == LEFT:
            BEAMS.append((position, DOWN))
    elif square == "\\":
        if direction == UP:
            BEAMS.append((position, LEFT))
        elif direction == RIGHT:
            BEAMS.append((position, DOWN))
        elif direction == DOWN:
            BEAMS.append((position, RIGHT))
        elif direction == LEFT:
            BEAMS.append((position, UP))

print(len(ENERGISED))
