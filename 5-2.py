import sys


flatmap = [(0, +0)]


class RangeMap:
    m: list[(int, int)]

    def __init__(self):
        self.m = [(0, +0), (9999999999999999999999, +0)]

    def add_range(self, dst, src, size):
        print(f"add_range({dst}, {src}, {size})")
        diff = dst - src
        start = src
        end = start + size
        print(f"  diff={diff} start={start} end={end}")
        print(self)
        print()

        for i in range(len(self.m)):
            self._check_invariants()

            ostart, odiff = self.m[i]
            oend, ndiff = self.m[i + 1]
            deep_start = ostart + odiff
            deep_end = oend + odiff

            print(
                f"start={start} end={end} ostart={ostart} oend={oend} odiff={odiff} ndiff={ndiff} deep_start={deep_start} deep_end={deep_end}"
            )

            # s  |--------|
            # ds |--------|
            # r  |--------|
            if start == deep_start and end == deep_end:
                print("case 1")
                self.m[i] = (ostart, odiff + diff)
                break
            # s  |-----|
            # ds |--------|
            # r  |-----|---|
            elif start == deep_start and end < deep_end:
                print("case 2")
                self.m[i] = (ostart, odiff + diff)
                self.m.insert(i + 1, (end, odiff))
                break
            # s  |------------|
            # ds |--------|
            # r  |---|--------|
            elif start == deep_start and end > deep_end:
                print("case 3")
                self.m[i] = (ostart, odiff + diff)
                start = deep_end
                continue
            # s     |---------|
            # ds |------------|
            # r  |--|---------|
            elif start > deep_start and end == deep_end:
                print("case 4")
                self.m.insert(i + 1, (start, odiff + diff))
                break
            # s     |-------|
            # ds |------------|
            # r  |--|-------|-|
            elif start > deep_start and end < deep_end:
                print("case 5")
                self.m.insert(i + 1, (start, odiff + diff))
                self.m.insert(i + 2, (end, odiff))
                break
            # s     |------------|
            # ds |------------|
            # r  |--|---------|--|
            elif start > deep_start and end > deep_end and start < deep_end:
                print("case 6")
                self.m.insert(i + 1, (start, odiff + diff))
                self.m[i + 2] = (oend, self.m[i + 2][1] + diff)
                self.m.insert(i + 3, (end, ndiff))
                break
            # s           |----|
            # ds |-----|
            # r  next
            elif start > deep_end:
                print("case 7")
                continue
            # s  |----|
            # ds         |-----|
            # r  next
            elif end < deep_start:
                print("case 8")
                continue
            else:
                raise Exception("unhandled case")

    def _check_invariants(self):
        for i in range(len(self.m) - 1):
            start, diff = self.m[i]
            end, _ = self.m[i + 1]
            assert start < end

    def get(self, index):
        for i in range(len(self.m) - 1):
            start, diff = self.m[i]
            end, _ = self.m[i + 1]
            if index >= start and index < end:
                return index + diff
        return index

    def __str__(self):
        lines = []
        for i in range(len(self.m) - 1):
            start, diff = self.m[i]
            lines.append(f"{start} {diff}")
        return "\n".join(lines)

    def __repr__(self):
        return str(self)


rm = RangeMap()

rm.add_range(50, 98, 2)
rm.add_range(52, 50, 48)

rm.add_range(0, 15, 37)
rm.add_range(37, 52, 2)
rm.add_range(39, 0, 15)

print(rm)
print()
print(rm.get(79))

sys.exit(0)


def read_section(input) -> bool:
    if input.readline() == "":
        return False

    while True:
        line = input.readline()
        if not line:
            break
        line = line.strip()
        if not line:
            break
        a, b, size = map(int, line.split(" "))
        rm.add_range(a, b, size)
        print(f"add_range({a}, {b}, {size})")

    return True


input = open("5.smallinput", "r")

# nums = list(map(int, input.readline().split(":")[1].strip().split(" ")))
# seed_ranges = [tuple(nums[i : i + 2]) for i in range(0, len(nums), 2)]
seeds = list(map(int, input.readline().split(":")[1].strip().split(" ")))

input.readline()  # skip empty line

while read_section(input):
    pass

smallest = 9999999999999999999999
# for start, length in seed_ranges:
for seed in seeds:
    location = rm.get(seed)
    if location < smallest:
        smallest = location
    print(f"seed {seed} -> location {location}")

print(smallest)
