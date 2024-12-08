from aoc_general import *

lines = read_input_day(6).split("\n")

DIRECTIONS = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0),
]

def solve_part_1():
    at_y = [ i for i in range(len(lines)) if any(c in lines[i] for c in "^>v<") ][0]
    at_x = [ lines[at_y].find(c) for c in "^>v<" if lines[at_y].find(c) != -1 ][0]
    at_dir = "^>v<".index(lines[at_y][at_x])

    been_on_locs = set()
    been_on_locs.add((at_x, at_y))
    lines[at_y] = lines[at_y][:at_x] + "." + lines[at_y][at_x + 1:]
    while True:
        next_x = at_x + DIRECTIONS[at_dir][0]
        next_y = at_y + DIRECTIONS[at_dir][1]

        if next_y < 0 or next_y >= len(lines) or next_x < 0 or next_x >= len(lines[next_y]):
            return len(been_on_locs)
        if lines[next_y][next_x] == "." :
            at_x = next_x
            at_y = next_y
            been_on_locs.add((at_x, at_y))
            continue
        if lines[next_y][next_x] == "#":
            at_dir = (at_dir + 1) % 4
            continue
        print(lines[next_y][next_x])

submit_result_day(6, 1, solve_part_1)

    