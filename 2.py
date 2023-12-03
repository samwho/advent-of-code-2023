target = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

possible = 0

for line in open("2.input"):
    line = line.strip()
    if not line:
        continue

    pre, rest = line.split(":", 2)

    id = int(pre.split(" ")[1])

    is_possible = True
    for turn in rest.split("; "):
        for pick in turn.split(", "):
            pick = pick.strip()
            print(pick)
            number, color = pick.split(" ", 2)
            color = color.strip()
            number = int(number.strip())

            if color in target and number > target[color]:
                is_possible = False
                break
        if not is_possible:
            break

    if is_possible:
        possible += id


print(possible)
