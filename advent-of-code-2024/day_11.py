from functools import lru_cache
from aoc_general import *

stones = [ int(s) for s in read_input_day(11).split(" ") ]


def change_stone(stones, index):
    if stones[index] == 0:
        stones[index] = 1
    elif len(str(stones[index])) % 2 == 0:
        value = str(stones[index])
        stones[index] = int(value[:len(value) // 2])
        stones.insert(index + 1, int(value[len(value) // 2:]))
    else:
        stones[index] = stones[index] * 2024
    return stones

@lru_cache(maxsize=None)
def change_stone_times(stone_value, times):
    if times == 0:
        return 1
    res = change_stone([ stone_value ], 0)
    return sum(change_stone_times(s, times-1) for s in res)


def solve_part_1():
    total = 0
    for s in stones:
        total += change_stone_times(s, 25)
    return total

def solve_part_2():
    total = 0
    for s in stones:
        total += change_stone_times(s, 75)
    return total

submit_result_day(11, 1, solve_part_1)

submit_result_day(11, 2, solve_part_2)

