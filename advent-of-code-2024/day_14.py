from aoc_general import *

robot_lines = read_input_day(14).split("\n")
# bathroom_size = (11, 7)
bathroom_size = (101, 103)
bathroom_middle = (bathroom_size[0] // 2, bathroom_size[1] // 2)

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

def for_each_position(robot_idx):
    has_been, time = set(), 0
    while True:
        x, y = move_robot(robot_idx, time)
        if (x, y) in has_been:
            break
        has_been.add((x, y))
        time += 1
        yield (x, y, time)

def period_at_position(robot_idx, position):
    total_positions = 0
    in_position_at_time = None
    for x, y, time in for_each_position(robot_idx):
        total_positions += 1
        if (x, y) == position:
            in_position_at_time = time
    if in_position_at_time is not None:
        return total_positions, in_position_at_time
    return None

def in_top_corners(x, y):
    from_tl = x + y
    if from_tl < (bathroom_size[0] - 1) // 2:
        return True
    from_tr = bathroom_size[0] - 1 - x + y
    if from_tr < (bathroom_size[0] - 1) // 2:
        return True
    return False

def solve_part_1():
    quadrants = amount_per_quadrant(100)
    return quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]

def solve_part_2_score():
    best_score, best_time = float("-inf"), 0

    try_seconds = 10403
    for time in range(try_seconds):
        robots = robots_after_time(time)

        # (4)
        # Check how many bots have a diagonal neighbor outwards or a horizontal one inwards
        bots_set = set(robots)
        score = 0
        for x, y in robots:
            is_left = x < bathroom_middle[0]
            xd_outwards = -1 if is_left else 1
            diagonal_outwards = (x + xd_outwards, y + 1)
            horizontal_inwards = (x - xd_outwards, y)
            if diagonal_outwards in bots_set or horizontal_inwards in bots_set:
                score += 1

        # (3)
        # Check how many bots are diagonal from top middle
        # top_middle = (bathroom_middle[0], 0)
        # is_diagonal = lambda x1, y1, x2, y2: abs(x1 - x2) == abs(y1 - y2)
        # bots_diagonal = [ (x, y) for x, y in robots if is_diagonal(x, y, top_middle[0], top_middle[1]) ]
        # score = len(bots_diagonal)

        # (2)
        # For each bot on the left size, see if it has a right size equivalent
        # right_bots = set([ (x, y) for x, y in robots if x > bathroom_middle[0] ])
        # left_bots = set([ (x, y) for x, y in robots if x < bathroom_middle[0] ])
        # bots_with_right = []
        # for x, y in left_bots:
        #     if (bathroom_size[0] - x - 1, y) in right_bots:
        #         bots_with_right.append((x, y))
        # score = len(bots_with_right)
        
        # (1)
        # # Make a map of amounts per row/col
        # robots_per_x = [ 0 ] * bathroom_size[0]
        # robots_per_y = [ 0 ] * bathroom_size[1]
        # for x, y in robots:
        #     robots_per_x[x] += 1
        #     robots_per_y[y] += 1
        # # First, check Xs are symetrical
        # left_x = list(reversed(robots_per_x[:bathroom_size[0] // 2]))
        # right_x = robots_per_x[bathroom_size[0] // 2 + 1:]
        # score = -sum([ abs(l - r) for l, r in zip(left_x, right_x) ])

        if score > best_score:
            print("New best score", score, "at time", time)
            best_score = score
            best_time = time

    print("Best score", best_score, "at time", best_time)
    return best_time


def solve_part_2():
    needed_positions = [
        (bathroom_middle[0], 0),
        (bathroom_size[0] - 1, 1),
        (bathroom_size[0] + 1, 1),
        (bathroom_size[0] - 2, 2),
        (bathroom_size[0] + 2, 2),
    ]

    for idx in range(len(robots)):
        total_period, in_position_at_time = period_at_position(idx, needed_positions[0])
        print("Robot", idx, "total period", total_period, "in position at time", in_position_at_time)


submit_result_day(14, 1, solve_part_1())

tree_after_time = solve_part_2_score()

print("Found tree after time", tree_after_time)

field = [ [ "." ] * bathroom_size[0] for _ in range(bathroom_size[1]) ]
for x, y in robots_after_time(tree_after_time):
    field[y][x] = "#"

print("\n".join([ "".join(row) for row in field ]))
print(tree_after_time)

submit_result_day(14, 2, tree_after_time)
        
