from aoc_general import *
from shared_py.grid import *
from multiprocessing import Pool

grid_str = read_input_day(20)
maze = Grid(grid_str)

# state will be (position, did_moves, cheated_positions)
def possible_moves(cost, state):
    at, cheated_positions = state
    for new_dir in range(4):
        new_pos = move(at, new_dir)
        if new_pos not in maze:
            continue
        if maze[new_pos] == "#" and len(cheated_positions) == 0:
            yield (cost + 1, (new_pos, (new_pos,)))
            continue
        # if len(cheated_positions) == 1:
        #     yield (cost + 1, (new_pos, (cheated_positions[0], new_pos)))
        #     continue
        if maze[new_pos] == "#":
            continue
        yield (cost + 1, (new_pos, cheated_positions))

def try_without_wall(xy):
    print(xy)
    maze_copy = maze.copy()
    old = maze[xy]
    if old == ".":
        return
    walls_around = 0
    for dx, dy in DIRECTIONS_4:
        if (xy[0] + dx, xy[1] + dy) not in maze_copy:
            walls_around += 1
        if maze_copy[(xy[0] + dx, xy[1] + dy)] == "#":
            walls_around += 1
    if walls_around == 3:
        return
    maze_copy[xy] = "."
    then_path = maze_copy.path("S", "E")
    return len(then_path) - 1

def solve_day_1():
    s = maze.find("S")
    e = maze.find("E")



    normal_duration = len(maze.path(s, e)) - 1
    possible_lengths = []
    todo_locations = list(iter(maze))[:10]
    print(todo_locations)
    pool = Pool(1)
    lengths = pool.map(try_without_wall, todo_locations)
    saved = [ l for l in lengths if l is not None and l < normal_duration ]
    more_than_100_saved = sum(1 for s in saved if s >= 100)
    return more_than_100_saved
    


    # start = (maze.find("S"), tuple())
    # _, _, back_map = maze.dijkstra(start, "E", possible_moves, True, True)
    # final_states = [ s for s in back_map.keys() if s[0] == maze.find("E") ]

    # normal_final_state = [ s for s in final_states if len(s[1]) == 0 ][0]
    # normal_duration = len(maze.reconstruct_path(back_map, normal_final_state)) - 1
    # print(normal_duration)

    # cheated_final_states = [ s for s in final_states if len(s[1]) > 0 ]
    # all_cheats_paths_per_state = [ list(maze.reconstruct_all_paths(back_map, s)) for s in cheated_final_states ]
    # all_cheat_paths = sum(all_cheats_paths_per_state, [])
    # cheat_path_lengths = [ len(path) - 1 for path in all_cheat_paths ]

    saved_time = [ normal_duration - l for l in possible_lengths if l < normal_duration ]
    more_than_100_saved = sum(1 for s in saved_time if s >= 100)
    return more_than_100_saved

print(solve_day_1())

# submit_result_day(20, 1, solve_day_1())
