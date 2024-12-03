from aoc_general import read_input_day
import re

lines = read_input_day(3).split("\n")

# Part 1:

def solve(do_enables):
    total = 0
    enabled = True


    for ln in lines:
        groups = re.findall(r"mul\([0-9]{1,3},[0-9]{1,3}\)|don't\(\)|do\(\)", ln)
        for group in groups:
            if group == "don't()":
                enabled = not do_enables
                continue
            if group == "do()":
                enabled = True
                continue
            if enabled:
                digits = re.findall(r"[0-9]{1,3}", group)
                total += int(digits[0]) * int(digits[1])

    return total

print(solve(False))
print(solve(True))

# import timeit

# print(str(timeit.timeit("solve(False)", globals=globals(), number=10000) / 10000 * 1000) + "ms")