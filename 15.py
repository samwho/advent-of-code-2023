def hash(s: str) -> int:
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h = h % 256
    return h


path = "15.input"
input = open(path).read().strip()

total = 0
for command in input.split(","):
    total += hash(command)
print(total)
