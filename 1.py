import re

word_numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
real_numbers = [str(i) for i in range(1, 10)]

numbers_re = "|".join(real_numbers + word_numbers)

first_re = rf"^.*?({numbers_re}).*$"
last_re = rf"^.*({numbers_re}).*?$"


def to_int(number):
    if number in word_numbers:
        return word_numbers.index(number) + 1
    return int(number)


total = 0
for line in open("1.input"):
    line = line.strip()
    if not line:
        continue

    first = re.match(first_re, line).group(1)
    last = re.match(last_re, line).group(1)

    total += int(f"{to_int(first)}{to_int(last)}")

print(total)
