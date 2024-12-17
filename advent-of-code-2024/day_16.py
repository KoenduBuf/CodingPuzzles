from aoc_general import *
from shared_py.grid import *

grid_str = read_input_day(16)
maze = Grid(grid_str)
at = maze.find("S")
maze[at] = "."

def possible_moves(cost, state):
    at, at_dir = state
    for new_dir in range(4):
        # Skip turning around
        if ((at_dir + 2) % 4) == new_dir:
            continue
        # Not changing direction is cheap
        new_pos = move(at, new_dir)
        if new_pos not in maze or maze[new_pos] == "#":
            continue
        if new_dir == at_dir:
            yield (cost + 1, (new_pos, new_dir))
            continue
        yield (cost + 1001, (new_pos, new_dir))

def solve_part_1():
    cost, _, _ = maze.dijkstra((at, 1), "E", possible_moves)
    return cost

def solve_part_2():
    _, last_state, back_map = maze.dijkstra((at, 1), "E", possible_moves)

    best_seats = set()
    from_stack = [ last_state ]
    while len(from_stack) > 0:
        back_from = from_stack.pop()
        best_seats.add(back_from[0])
        cost_and_back_options = back_map[back_from]
        if cost_and_back_options is None:
            continue
        for back_option in cost_and_back_options[1]:
            from_stack.append(back_option)

    return len(best_seats)


submit_result_day(16, 1, solve_part_1())

submit_result_day(16, 2, solve_part_2())


