from contextlib import contextmanager
from typing import Generator, Literal, Optional

DEBUG = False


@contextmanager
def no_debug() -> Generator[None, None, None]:
    global DEBUG
    prev = DEBUG
    DEBUG = False
    yield
    DEBUG = prev


def debug(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


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


grid: Grid = list(
    map(lambda line: list(iter(line.strip())), open("10.input").read().splitlines())
)


def is_connected(a: Point, b: Point) -> bool:
    if not abs(a[0] - b[0]) <= 1 and abs(a[1] - b[1]) <= 1:
        debug(f"{a} and {b} are not adjacent")
        return False

    aval = grid[a[1]][a[0]]
    bval = grid[b[1]][b[0]]

    direction = (b[0] - a[0], b[1] - a[1])
    if direction == UP:
        connected = aval in HAS_UP and bval in HAS_DOWN
        debug(f"checking {a} -> {b} ({aval} -> {bval}) (UP) connected={connected}")
        return connected
    elif direction == DOWN:
        connected = aval in HAS_DOWN and bval in HAS_UP
        debug(f"checking {a} -> {b} ({aval} -> {bval}) (DOWN) connected={connected}")
        return connected
    elif direction == LEFT:
        connected = aval in HAS_LEFT and bval in HAS_RIGHT
        debug(f"checking {a} -> {b} ({aval} -> {bval}) (LEFT) connected={connected}")
        return connected
    elif direction == RIGHT:
        connected = aval in HAS_RIGHT and bval in HAS_LEFT
        debug(f"checking {a} -> {b} ({aval} -> {bval}) (RIGHT) connected={connected}")
        return connected
    raise ValueError("Invalid direction")


def find_start() -> Point:
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "S":
                return (x, y)
    raise ValueError("No start found")


def neighbours(point: Point) -> Generator[Point, None, None]:
    x, y = point
    if x > 0:
        yield (x - 1, y)
    if x < len(grid[y]) - 1:
        yield (x + 1, y)
    if y > 0:
        yield (x, y - 1)
    if y < len(grid) - 1:
        yield (x, y + 1)


def valid_neighbours(point: Point) -> Generator[Point, None, None]:
    debug(f"valid_neighbours({point})")
    val = grid[point[1]][point[0]]
    debug(f"val = {val}")
    if val == ".":
        raise ValueError(f"{point} ceci n'est une pipe")

    for other in neighbours(point):
        oval = grid[other[1]][other[0]]
        debug(f"checking {other} ({oval})")
        if is_connected(point, other):
            debug(f"{other} is connected")
            yield other


class Node:
    length: int = 0
    parent: Optional["Node"]
    point: Point

    def __init__(self, point: Point) -> None:
        self.parent = None
        self.point = point

    def add(self, point: Point) -> "Node":
        node = Node(point)
        node.parent = self
        node.length = self.length + 1
        return node

    def is_root(self) -> bool:
        return self.parent is None

    def get_root(self) -> "Node":
        if self.is_root():
            return self

        parent = self.parent
        while parent:
            if parent.is_root():
                return parent
            parent = parent.parent
        raise ValueError("No root found")

    def is_loop(self) -> bool:
        if self.length < 2:
            return False
        root = self.get_root()
        debug(f"root = {root}, self = {self}")
        return root.point == self.point

    def path(self) -> list[Point]:
        p = []
        node = self
        while not node.is_root():
            p.append(node.point)
            node = node.parent
        return list(reversed(p))

    def __str__(self) -> str:
        return f"{self.point}"


frontier = [Node(find_start())]
while True:
    node = frontier.pop()
    if node.is_loop():
        print(f"{node.path()}")
        print(f"length = {node.length}")
        print(f"further = {node.length / 2}")
        break

    for neighbour in valid_neighbours(node.point):
        nval = grid[neighbour[1]][neighbour[0]]
        if (not node.parent) or neighbour != node.parent.point:
            frontier.append(node.add(neighbour))
