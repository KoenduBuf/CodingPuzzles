from aoc_general import *
from functools import lru_cache

can_use, all_to_make = read_input_day(19).split("\n\n")

can_use = can_use.split(", ")
can_use_set = set(can_use)
all_to_make = all_to_make.split("\n")

@lru_cache(maxsize=None)
def can_make_pattern(to_make):
    if len(to_make) == 0:
        return 1
    ways_to_make = 0
    for to_use in can_use:
        if to_make.startswith(to_use):
            ways_to_make += can_make_pattern(to_make[len(to_use):])
    return ways_to_make

def solve_part_1():
    can_solve = 0
    for pattern in all_to_make:
        if can_make_pattern(pattern) > 0:
            can_solve += 1
    return can_solve

def solve_part_2():
    can_make_ways = 0
    for pattern in all_to_make:
        can_make_ways += can_make_pattern(pattern)
    return can_make_ways

submit_result_day(19, 1, solve_part_1())

submit_result_day(19, 2, solve_part_2())
