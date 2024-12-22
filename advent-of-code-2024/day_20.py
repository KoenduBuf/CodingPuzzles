from aoc_general import *
from shared_py.grid import *


grid_str = read_input_day(20)
maze = Grid(grid_str)


def solve_part_1_remove_walls():
    s = maze.find("S")
    e = maze.find("E")

    normal_duration = len(maze.path(s, e)) - 1
    saved_lengths = []

    for x, y in maze:
        print(x, y)
        # Go over all walls
        if maze[x, y] != "#":
            continue
        # Check if there is 3 walls around it
        walls_around = 0
        for new_dir in range(4):
            new_pos = move((x, y), new_dir)
            if new_pos not in maze:
                walls_around += 1
            elif maze[new_pos] == "#":
                walls_around += 1
        if walls_around >= 3:
            continue
        # Try with cheat (remove wall)
        maze[x, y] = "."
        l = len(maze.path(s, e)) - 1
        maze[x, y] = "#"
        saved = normal_duration - l
        if saved >= 100:
            saved_lengths.append(saved)

    return len(saved_lengths)

def solve_part_1_cheating():
    s = maze.find("S")
    e = maze.find("E")

    normal_duration = len(maze.path(s, e)) - 1
    print(normal_duration)

    saved_lengths = []
    start = (maze.find("S"), tuple())

    # state will be (position, did_moves, cheated_positions)
    not_allowed_to_cheat_locations = set()
    def possible_moves(cost, state):
        at, cheated_positions = state
        for new_dir in range(4):
            new_pos = move(at, new_dir)
            if new_pos not in maze:
                continue
            if maze[new_pos] == "#" and len(cheated_positions) == 0:
                if new_pos in not_allowed_to_cheat_locations:
                    continue
                yield (cost + 1, (new_pos, (new_pos,)))
                continue
            # if len(cheated_positions) == 1:
            #     yield (cost + 1, (new_pos, (cheated_positions[0], new_pos)))
            #     continue
            if maze[new_pos] == "#":
                continue
            yield (cost + 1, (new_pos, cheated_positions))

    while True:
        next_fastest_cost, final_state, _ = maze.dijkstra(start, "E", possible_moves)
        cheat_spot = final_state[1][0]
        not_allowed_to_cheat_locations.add(cheat_spot)
        saved = normal_duration - next_fastest_cost
        print(cheat_spot, next_fastest_cost, saved)
        if saved < 100:
            break
        saved_lengths.append(saved)
    
    return len(saved_lengths)

def solve_part_2_jump_map(cheat_distance=20):
    normal_duration = len(maze.path("S", "E")) - 1
    to_start_map = maze.flood_fill_map("S")
    to_end_map = maze.flood_fill_map("E")
    
    all_time_saves = []
    CHEAT_DISTANCE = cheat_distance
    
    for x, y in maze:
        if maze[x, y] == "#":
            continue
        # Assume we start to cheat from x, y
        # Then first we check how long it would take to go from S to x, y
        time_to_xy = to_start_map[x, y]

        # Then for each wall in a radius of 'CHEAT_DISTANCE' around x, y
        # We check how long it would be to go to E
        for dx in range(-CHEAT_DISTANCE, CHEAT_DISTANCE + 1):
            for dy in range(-CHEAT_DISTANCE, CHEAT_DISTANCE + 1):
                if dx == 0 and dy == 0:
                    continue
                new_x, new_y = x + dx, y + dy
                this_cheat_distance = abs(dx) + abs(dy)
                if this_cheat_distance > CHEAT_DISTANCE:
                    continue
                if (new_x, new_y) not in maze:
                    continue
                if maze[new_x, new_y] == "#":
                    continue
                # For each end point
                time_to_e = to_end_map[new_x, new_y]
                total_race_length = time_to_xy + this_cheat_distance + time_to_e
                time_saved = normal_duration - total_race_length
                all_time_saves.append(time_saved)
    
    at_least_100_saves = [ s for s in all_time_saves if s >= 100 ]
    return len(at_least_100_saves)


submit_result_day(20, 1, solve_part_2_jump_map(2))

submit_result_day(20, 2, solve_part_2_jump_map(20))

