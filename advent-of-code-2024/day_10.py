from aoc_general import *

DIRECTIONS = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0),
]

lines = [ [ int(n) for n in ln ] for ln in read_input_day(10).split("\n") ]

def to_ends_map(lines, use_set=False):
    map = [ [ set() if use_set else 0 for _ in range(len(lines[y])) ] for y in range(len(lines)) ]

    for num in reversed(range(0, 10)):
        for y in range(len(lines)):
            for x in range(len(lines[y])):
                if lines[y][x] == num:
                    
                    if num == 9:
                        if use_set:
                            map[y][x].add((x, y))
                        else:
                            map[y][x] = 1
                        continue

                    for d in DIRECTIONS:
                        if y + d[1] < 0 or y + d[1] >= len(lines) or x + d[0] < 0 or x + d[0] >= len(lines[y]):
                            continue
                        if lines[y + d[1]][x + d[0]] == num + 1:
                            if use_set:
                                map[y][x].update(map[y + d[1]][x + d[0]])
                            else:
                                map[y][x] += map[y + d[1]][x + d[0]]
    return map

def solve_part_1():
    map = to_ends_map(lines, True)
    total = 0
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == 0:
                total += len(map[y][x])
    return total

def solve_part_2():
    map = to_ends_map(lines, False)
    total = 0
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == 0:
                total += map[y][x]
    return total

submit_result_day(10, 1, solve_part_1)

submit_result_day(10, 2, solve_part_2)
