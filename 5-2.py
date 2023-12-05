def debug(*args):
    return
    print(*args)


class RangeMap:
    ranges: [(int, int, int)]

    def __init__(self):
        self.ranges = []

    def _check_result_invariants(self, results):
        for a1, a2 in results:
            assert a1 < a2, f"{a1} < {a2}, {results}"

    def add_range(self, src: int, dst: int, size: int):
        self.ranges.append((src, dst, size))
        self.ranges.sort(key=lambda x: x[0])

    def get(self, index_range: (int, int)) -> list[(int, int)]:
        debug(f"get({index_range})")
        debug(f"ranges: {self.ranges}")

        a1, a2 = index_range
        assert a1 <= a2
        results = []
        for src, dst, size in self.ranges:
            b1 = src
            b2 = src + size
            diff = dst - src

            debug(f"a1: {a1}, a2: {a2}, b1: {b1}, b2: {b2}, diff: {diff}")

            # a |------|
            # b          |------|
            if a2 <= b1:
                debug("case 1")
                results.append((a1, a2))
                self._check_result_invariants(results)
                break
            # a          |------|
            # b |------|
            if a1 >= b2:
                debug("case 2")
                continue
            # a |------|
            # b |--------|
            if a1 == b1 and a2 <= b2:
                debug("case 3")
                results.append((a1 + diff, a2 + diff))
                self._check_result_invariants(results)
                break
            # a |---------|
            # b |------|
            if a1 == b1 and a2 > b2:
                debug(f"case 4: {a1} == {b1} and {a2} > {b2}")
                results.append((a1 + diff, b2 + diff))
                debug(f"added {a1 + diff}, {b2 + diff}")
                a1 = b2
                self._check_result_invariants(results)
                continue

            # a |------|
            # b    |------|
            if a1 < b1 and a2 <= b2:
                debug("case 5")
                results.append((a1, b1))
                results.append((b1 + diff, a2 + diff))
                self._check_result_invariants(results)
                break

            # a |----------|
            # b   |-----|
            if a1 < b1 and a2 > b2:
                debug("case 6")
                results.append((a1, b1))
                results.append((b1 + diff, b2 + diff))
                self._check_result_invariants(results)
                a1 = b2
                continue

            # a    |------|
            # b |------|
            if a1 > b1 and a2 >= b2 and a1 < b2:
                debug("case 7")
                results.append((b1, a1))
                results.append((a1 + diff, b2 + diff))
                self._check_result_invariants(results)
                a1 = b2
                continue

            # a    |----|
            # b |----------|
            if a1 > b1 and a2 < b2:
                debug("case 8")
                results.append((a1 + diff, a2 + diff))
                self._check_result_invariants(results)
                break

            debug("missed case")

        if not results:
            results.append((a1, a2))
            self._check_result_invariants(results)

        debug(f"return: {results}")
        return results

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
        dst, src, size = map(int, line.split(" "))
        rm.add_range(src, dst, size)

    return name, rm


input = open("5.input", "r")

nums = list(map(int, input.readline().split(":")[1].strip().split(" ")))
seed_ranges = [tuple(nums[i : i + 2]) for i in range(0, len(nums), 2)]

input.readline()  # skip empty line

maps = {}
while True:
    name, rm = read_section(input)
    if name == "":
        break

    frm, to = name.split("-to-")
    maps[(frm, to)] = rm

map_list = [
    maps[("seed", "soil")],
    maps[("soil", "fertilizer")],
    maps[("fertilizer", "water")],
    maps[("water", "light")],
    maps[("light", "temperature")],
    maps[("temperature", "humidity")],
    maps[("humidity", "location")],
]

locations = []

for start, size in seed_ranges:
    ranges = [(start, start + size)]
    for map in map_list:
        new_ranges = []
        for range in ranges:
            new_ranges.extend(map.get(range))
        ranges = new_ranges

    ranges.sort(key=lambda x: x[0])
    locations.append(ranges[0])

locations.sort(key=lambda x: x[0])
print(locations[0][1])
