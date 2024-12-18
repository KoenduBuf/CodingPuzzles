from aoc_general import *
from shared_py.grid import *

byte_drops = [ tuple(int(n) for n in ln.split(",")) for ln in read_input_day(18).split("\n") ]
memory_size = (71, 71)

def maze_at_time(time):
    maze = Grid(".", *memory_size)
    for x, y in byte_drops[:time]:
        maze[(x, y)] = "#"
    return maze

def solve_part_1():
    maze = maze_at_time(1024)
    goal = tuple(m-1 for m in memory_size)
    path = maze.path((0, 0), goal)
    return len(path) - 1

def solve_part_2():
    goal = tuple(m-1 for m in memory_size)
    for i in range(0, len(byte_drops)):
        maze = maze_at_time(i)
        path = maze.path((0, 0), goal)
        if path is None:
            return ",".join(str(n) for n in byte_drops[i-1])

submit_result_day(18, 1, solve_part_1())

submit_result_day(18, 2, solve_part_2(), allow_non_numeric=True)
