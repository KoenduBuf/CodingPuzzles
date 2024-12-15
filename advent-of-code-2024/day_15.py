from aoc_general import *
from shared_py.grid import *

maze_str, moves_str = read_input_day(15).split("\n\n")



def can_push(maze, from_pos, direction):
    to = move_and_push(maze, from_pos, direction, True)
    return to != from_pos

def do_push(maze, from_pos, direction):
    pushed_to = move_and_push(maze, from_pos, direction, False)
    maze[pushed_to] = maze[from_pos]
    maze[from_pos] = "."

def try_then_do_push(maze, positions, direction, dry_run):
    unique_positions = [ pos for i, pos in enumerate(positions) if pos not in positions[:i] ]
    if not all([can_push(maze, pos, direction) for pos in unique_positions]):
        return False
    if dry_run:
        return True
    for pos in unique_positions:
        do_push(maze, pos, direction)
    return True

def move_and_push(maze, from_pos, direction, dry_run):
    new_pos = move(from_pos, direction)
    # Check if we can move, return the position we moved to
    if maze[new_pos] == "#":
        return from_pos
    if maze[new_pos] == ".":
        return new_pos
    # For crates, check if we can push them
    if maze[new_pos] == "O":
        if try_then_do_push(maze, [ new_pos ], direction, dry_run):
            return new_pos
        return from_pos
    if maze[new_pos] == "[":
        if direction == 3:
            if try_then_do_push(maze, [ new_pos ], direction, dry_run):
                return new_pos
        elif try_then_do_push(maze, [ (new_pos[0] + 1, new_pos[1]), new_pos ], direction, dry_run):
            return new_pos
        return from_pos
    if maze[new_pos] == "]":
        if direction == 1:
            if try_then_do_push(maze, [ new_pos ], direction, dry_run):
                return new_pos
        elif try_then_do_push(maze, [ (new_pos[0] - 1, new_pos[1]), new_pos ], direction, dry_run):
            return new_pos
        return from_pos
    raise Exception(f"Unknown character at {new_pos}: {maze[new_pos]}")

def boxes_gps_sum(maze):
    locs = maze.find_all("O") + maze.find_all("[")
    return sum([box_loc[0] + 100 * box_loc[1] for box_loc in locs])

def solve_part_1():
    maze = Grid(maze_str)
    at = maze.find("@")
    maze[at] = "."
    pos = at
    for move in to_directions(moves_str):
        pos = move_and_push(maze, pos, move, False)
    return boxes_gps_sum(maze)

def solve_part_2():
    double_wide_maze = maze_str\
        .replace("#", "##")\
        .replace("O", "[]")\
        .replace(".", "..")\
        .replace("@", "@.")
    maze = Grid(double_wide_maze)
    at = maze.find("@")
    maze[at] = "."
    pos = at
    for move in to_directions(moves_str):
        pos = move_and_push(maze, pos, move, False)
    return boxes_gps_sum(maze)

submit_result_day(15, 1, solve_part_1)

submit_result_day(15, 2, solve_part_2)
