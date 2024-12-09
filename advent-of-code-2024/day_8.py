from aoc_general import *

lines = read_input_day(8).split("\n")

# Get antennas
antennas = {}
for y in range(len(lines)):
    for x in range(len(lines[y])):
        if lines[y][x] != ".":
            antennas.setdefault(lines[y][x], []).append((x, y))

def is_in_bounds(xy):
    return xy[1] >= 0 and xy[1] < len(lines) and xy[0] >= 0 and xy[0] < len(lines[y])

def for_each_pair():
    for _, coords in antennas.items():
        if len(coords) == 1:
            continue
        for l in coords:
            for r in coords:
                if l[0] > r[0]:
                    continue
                if l[0] == r[0] and l[1] >= r[1]:
                    continue
                yield l, r


def solve_part_1():
    total_antinodes = set()

    for l, r in for_each_pair():
        dx = r[0] - l[0]
        dy = r[1] - l[1]
        anti_1 = (l[0] - dx, l[1] - dy)
        anti_2 = (r[0] + dx, r[1] + dy)
        if is_in_bounds(anti_1):
            total_antinodes.add(anti_1)
        if is_in_bounds(anti_2):
            total_antinodes.add(anti_2)
        
    return len(total_antinodes)

def solve_part_2():
    total_antinodes = set()

    for l, r in for_each_pair():
        dx = r[0] - l[0]
        dy = r[1] - l[1]

        next_l = (l[0], l[1])
        while True:
            if not is_in_bounds(next_l):
                break
            total_antinodes.add(next_l)
            next_l = (next_l[0] - dx, next_l[1] - dy)
            # print("next_l", next_l)

        next_r = (r[0], r[1])
        while True:
            if not is_in_bounds(next_r):
                break
            total_antinodes.add(next_r)
            next_r = (next_r[0] + dx, next_r[1] + dy)
        
    return len(total_antinodes)

submit_result_day(8, 1, solve_part_1)

submit_result_day(8, 2, solve_part_2)
