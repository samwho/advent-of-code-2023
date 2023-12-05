from pprint import pprint


class RangeMap:
    ranges: [(int, int, int)]

    def __init__(self):
        self.ranges = []

    def add_range(self, astart, bstart, size):
        self.ranges.append((astart, bstart, size))
        self.ranges.sort(key=lambda x: x[0])

    def get(self, index):
        for astart, bstart, size in self.ranges:
            if index >= bstart and index < bstart + size:
                return astart + (index - bstart)
        return index

    def __str__(self):
        return str(self.ranges)

    def __repr__(self):
        return str(self.ranges)


def read_section(input) -> (str, RangeMap):
    name = input.readline().strip().split(" ")[0]

    rm = RangeMap()
    while True:
        line = input.readline()
        if not line:
            break
        line = line.strip()
        if not line:
            break
        a, b, size = map(int, line.split(" "))
        rm.add_range(a, b, size)

    return name, rm


input = open("5.input", "r")

seeds = list(map(int, input.readline().split(":")[1].strip().split(" ")))

input.readline()  # skip empty line

maps = {}
while True:
    name, rm = read_section(input)
    if name == "":
        break

    frm, to = name.split("-to-")
    maps[(frm, to)] = rm

locations = []
for seed in seeds:
    soil = maps[("seed", "soil")].get(seed)
    fertilizer = maps[("soil", "fertilizer")].get(soil)
    water = maps[("fertilizer", "water")].get(fertilizer)
    light = maps[("water", "light")].get(water)
    temperature = maps[("light", "temperature")].get(light)
    humidity = maps[("temperature", "humidity")].get(temperature)
    location = maps[("humidity", "location")].get(humidity)
    locations.append(location)

locations.sort()
print(locations[0])
