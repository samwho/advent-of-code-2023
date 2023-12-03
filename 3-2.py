from collections import defaultdict


grid = []
gears = defaultdict(lambda: defaultdict(list))
numbers = defaultdict(dict)


def is_gear(val):
    return val == "*"


def find_adjacent_gear(i, j, grid):
    if i > 0 and is_gear(grid[i - 1][j]):
        return (i - 1, j)
    if i < len(grid) - 1 and is_gear(grid[i + 1][j]):
        return (i + 1, j)
    if j > 0 and is_gear(grid[i][j - 1]):
        return (i, j - 1)
    if j < len(grid[i]) - 1 and is_gear(grid[i][j + 1]):
        return (i, j + 1)
    if i > 0 and j > 0 and is_gear(grid[i - 1][j - 1]):
        return (i - 1, j - 1)
    if i > 0 and j < len(grid[i]) - 1 and is_gear(grid[i - 1][j + 1]):
        return (i - 1, j + 1)
    if i < len(grid) - 1 and j > 0 and is_gear(grid[i + 1][j - 1]):
        return (i + 1, j - 1)
    if i < len(grid) - 1 and j < len(grid[i]) - 1 and is_gear(grid[i + 1][j + 1]):
        return (i + 1, j + 1)
    return None


for line in open("3.input"):
    grid.append(list(line.strip()))

for i, row in enumerate(grid):
    current_num = ""
    adjacent_gear = None
    for j, col in enumerate(row):
        if col.isnumeric():
            current_num += col
            if not adjacent_gear:
                adjacent_gear = find_adjacent_gear(i, j, grid)
        else:
            if current_num == "":
                continue
            num = int(current_num)
            if adjacent_gear:
                numbers[i][j] = {"num": num, "adjacent": adjacent_gear}
            adjacent_gear = None
            current_num = ""
    if current_num != "":
        num = int(current_num)
        if adjacent_gear:
            numbers[i][len(row) - 1] = {"num": num, "adjacent": adjacent_gear}

for i, row in numbers.items():
    for j, col in row.items():
        if numbers[i][j]:
            num = numbers[i][j]["num"]
            adjacent = numbers[i][j]["adjacent"]
            gears[adjacent[0]][adjacent[1]].append(num)

total = 0
for i, row in gears.items():
    for j, col in row.items():
        if len(gears[i][j]) == 2:
            total += gears[i][j][0] * gears[i][j][1]

print(total)
