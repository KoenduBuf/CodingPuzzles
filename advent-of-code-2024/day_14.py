from aoc_general import *

robot_lines = read_input_day(14).split("\n")
bathroom_size = tuple(11, 7)

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


def get_quadrant(x, y):
    left = x < (bathroom_size[0] - 1) / 2
    top = y < (bathroom_size[1] - 1) / 2
    return left + 2 * top

def amount_per_quadrant(after_time):
    quadrants = [ [] ] * 4
    for idx in range(len(robots)):
        x, y = move_robot(idx, after_time)
        q = get_quadrant(x, y)
        quadrants[q] += 1
    return quadrants

def solve_part_1():
    quadrants = amount_per_quadrant(1000)
    return quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]

print(solve_part_1())


