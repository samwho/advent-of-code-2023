from typing import Literal, cast

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
Direction = tuple[int, int]
Beam = tuple[Position, Direction]

UP: Direction = (-1, 0)
DOWN: Direction = (1, 0)
LEFT: Direction = (0, -1)
RIGHT: Direction = (0, 1)


def read_grid(path) -> Grid:
    return cast(Grid, [list(line.strip()) for line in open(path)])


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


def solve(grid: Grid, beams: list[Beam]) -> int:
    energised: set[Position] = set([b[0] for b in beams if is_in_bounds(grid, b[0])])
    seen: set[Beam] = set([b for b in beams if is_in_bounds(grid, b[0])])

    while True:
        # print(len(BEAMS))
        # print_grid(grid, ENERGISED, BEAMS)
        # input()
        if len(beams) == 0:
            break

        position, direction = beams.pop()
        position = move(position, direction)
        if (position, direction) in seen:
            continue
        seen.add((position, direction))
        if not is_in_bounds(grid, position):
            continue

        energised.add(position)

        square = get_square(grid, position)

        if square == ".":
            beams.append((position, direction))
        elif square == "|":
            if direction in [UP, DOWN]:
                beams.append((position, direction))
            else:
                beams.append((position, UP))
                beams.append((position, DOWN))
        elif square == "-":
            if direction in [LEFT, RIGHT]:
                beams.append((position, direction))
            else:
                beams.append((position, LEFT))
                beams.append((position, RIGHT))
        elif square == "/":
            if direction == UP:
                beams.append((position, RIGHT))
            elif direction == RIGHT:
                beams.append((position, UP))
            elif direction == DOWN:
                beams.append((position, LEFT))
            elif direction == LEFT:
                beams.append((position, DOWN))
        elif square == "\\":
            if direction == UP:
                beams.append((position, LEFT))
            elif direction == RIGHT:
                beams.append((position, DOWN))
            elif direction == DOWN:
                beams.append((position, RIGHT))
            elif direction == LEFT:
                beams.append((position, UP))

    return len(energised)


m = 0
for y in range(len(grid)):
    a = solve(grid, [((y, -1), RIGHT)])
    if a > m:
        m = a
    a = solve(grid, [((y, len(grid)), LEFT)])
    if a > m:
        m = a

for x in range(len(grid[0])):
    a = solve(grid, [((-1, x), DOWN)])
    if a > m:
        m = a
    a = solve(grid, [((len(grid), x), UP)])
    if a > m:
        m = a

print(m)
