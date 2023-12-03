from collections import defaultdict


power = 0
for line in open("2.input"):
    line = line.strip()
    if not line:
        continue

    pre, rest = line.split(":", 2)

    id = int(pre.split(" ")[1])

    is_possible = True
    min_color = defaultdict(int)
    for turn in rest.split("; "):
        for pick in turn.split(", "):
            pick = pick.strip()
            number, color = pick.split(" ", 2)
            color = color.strip()
            number = int(number.strip())

            if number > min_color[color]:
                min_color[color] = number

    power += min_color["red"] * min_color["green"] * min_color["blue"]


print(power)
