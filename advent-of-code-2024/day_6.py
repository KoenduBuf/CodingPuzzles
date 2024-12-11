from aoc_general import *

DIRECTIONS = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0),
]

def read_start():
    lines = read_input_day(6).split("\n")
    at_y = [ i for i in range(len(lines)) if any(c in lines[i] for c in "^>v<") ][0]
    at_x = [ lines[at_y].find(c) for c in "^>v<" if lines[at_y].find(c) != -1 ][0]
    at_dir = "^>v<".index(lines[at_y][at_x])
    lines[at_y] = lines[at_y][:at_x] + "." + lines[at_y][at_x + 1:]
    return lines, at_x, at_y, at_dir

def walk(lines, at_x, at_y, at_dir) -> tuple[int, int, int] | None:
    next_x = at_x + DIRECTIONS[at_dir][0]
    next_y = at_y + DIRECTIONS[at_dir][1]
    if next_y < 0 or next_y >= len(lines) or next_x < 0 or next_x >= len(lines[next_y]):
        return None
    if lines[next_y][next_x] == "." :
        return (next_x, next_y, at_dir)
    if lines[next_y][next_x] == "#":
        return (at_x, at_y, (at_dir + 1) % 4)
    raise Exception("Should not reach here")

def solve_part_1():
    lines, at_x, at_y, at_dir = read_start()
    been_on_locs = set()
    been_on_locs.add((at_x, at_y))
    while True:
        w = walk(lines, at_x, at_y, at_dir)
        if w is None:
            return len(been_on_locs)
        at_x, at_y, at_dir = w
        been_on_locs.add((at_x, at_y))
    

def solve_part_2():
    lines, start_x, start_y, start_dir = read_start()
    at_x, at_y, at_dir = start_x, start_y, start_dir
    org_lines = lines.copy()

    def test_looping(lines, from_x, from_y, from_dir):
        # See if we end up in a loop
        been_in_state = set()
        while True:
            been_in_state.add((from_x, from_y, from_dir))
            w = walk(lines, from_x, from_y, from_dir)
            if w is None:
                return False
            from_x, from_y, from_dir = w
            if (from_x, from_y, from_dir) in been_in_state:
                return True
        raise Exception("Should not reach here")

    def would_be_in_a_loop(lines, at_x, at_y):
        now_is = lines[at_y][at_x]
        lines[at_y] = lines[at_y][:at_x] + "#" + lines[at_y][at_x + 1:]
        looping = test_looping(lines, start_x, start_y, start_dir)
        lines[at_y] = lines[at_y][:at_x] + now_is + lines[at_y][at_x + 1:]
        return looping

    try_obstructions = []
    while True:
        w = walk(lines, at_x, at_y, at_dir)
        if w is None:
            break
        at_x, at_y, at_dir = w
        try_obstructions.append((at_x, at_y, at_dir))

    obstruction_locs = set()
    for obs in try_obstructions:
        at_x, at_y, at_dir = obs
        if would_be_in_a_loop(lines, at_x, at_y):
            obstruction_locs.add((at_x, at_y))

    if (start_x, start_y) in obstruction_locs:
        obstruction_locs.remove((start_x, start_y))
    return len(obstruction_locs)
        

submit_result_day(6, 1, solve_part_1)

submit_result_day(6, 2, solve_part_2)
