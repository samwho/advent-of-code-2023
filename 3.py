grid = []


def is_part(val):
    if val.isnumeric():
        return False
    if val == ".":
        return False
    return True


def has_adjacent_part(i, j, grid):
    if i > 0 and is_part(grid[i - 1][j]):
        return True
    if i < len(grid) - 1 and is_part(grid[i + 1][j]):
        return True
    if j > 0 and is_part(grid[i][j - 1]):
        return True
    if j < len(grid[i]) - 1 and is_part(grid[i][j + 1]):
        return True
    if i > 0 and j > 0 and is_part(grid[i - 1][j - 1]):
        return True
    if i > 0 and j < len(grid[i]) - 1 and is_part(grid[i - 1][j + 1]):
        return True
    if i < len(grid) - 1 and j > 0 and is_part(grid[i + 1][j - 1]):
        return True
    if i < len(grid) - 1 and j < len(grid[i]) - 1 and is_part(grid[i + 1][j + 1]):
        return True
    return False


for line in open("3.input"):
    grid.append(list(line.strip()))

total = 0

for i, row in enumerate(grid):
    current_num = ""
    adjacent_part = False
    for j, col in enumerate(row):
        if col.isnumeric():
            current_num += col
            if has_adjacent_part(i, j, grid):
                adjacent_part = True
        else:
            if current_num == "":
                continue
            num = int(current_num)
            print(num, adjacent_part)
            if adjacent_part:
                total += num
            adjacent_part = False
            current_num = ""
    if current_num != "":
        num = int(current_num)
        print(num, adjacent_part)
        if adjacent_part:
            total += num

print(total)
