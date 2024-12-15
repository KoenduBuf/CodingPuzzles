from aoc_general import *

robot_lines = read_input_day(14).split("\n")
# bathroom_size = (11, 7)
bathroom_size = (101, 103)

# [ ((sx, sy), (dx, dy)), ... ]

robots = [
    [
        tuple(
            int(x)
            for x in xy[2:].split(",")
        )
        for xy in ln.split(" ")
    ]
    for ln in robot_lines
]

def move_robot(idx, time):
    start_x, start_y = robots[idx][0]
    dx, dy = robots[idx][1]
    endx = (start_x + time * dx) % bathroom_size[0]
    endy = (start_y + time * dy) % bathroom_size[1]
    return (endx, endy)

def robots_after_time(time):
    return [ move_robot(idx, time) for idx in range(len(robots)) ]

def get_quadrant(x, y):
    middle_x = (bathroom_size[0] - 1) / 2
    middle_y = (bathroom_size[1] - 1) / 2
    if x == middle_x or y == middle_y:
        return -1
    return int(x < middle_x) + 2 * int(y < middle_y)

def amount_per_quadrant(after_time):
    quadrants = [ 0 ] * 4
    for idx in range(len(robots)):
        x, y = move_robot(idx, after_time)
        q = get_quadrant(x, y)
        if q == -1:
            continue
        quadrants[q] += 1
    return quadrants

def solve_part_1():
    quadrants = amount_per_quadrant(100)
    return quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]

def solve_part_2():
    try_seconds = 10000000
    for time in range(try_seconds):
        if time % 10000 == 0:
            print(f"{time / try_seconds * 100}%")
        robots = robots_after_time(time)
        # Make a map of amounts per row/col
        robots_per_x = [ 0 ] * bathroom_size[0]
        robots_per_y = [ 0 ] * bathroom_size[1]
        for x, y in robots:
            robots_per_x[x] += 1
            robots_per_y[y] += 1
        # First, check Xs are symetrical
        left_x = robots_per_x[:bathroom_size[0] // 2]
        right_x = robots_per_x[bathroom_size[0] // 2 + 1:]
        if left_x != list(reversed(right_x)):
            continue
        return time
        

submit_result_day(14, 1, solve_part_1())

print(solve_part_2())

