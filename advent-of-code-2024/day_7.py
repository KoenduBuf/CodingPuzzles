from aoc_general import *

SIGMA = 0.00000000001

lines = read_input_day(7).split("\n")
combos = [ ( int(line.split(": ")[0]), [ int(n) for n in line.split(": ")[1].split(" ") ]) for line in lines ]

# Part 1

def is_possible_1(result, with_nums):
    if len(with_nums) == 1:
        return abs(with_nums[0] - result) < SIGMA
    return is_possible_1(result - with_nums[-1], with_nums[:-1]) or is_possible_1(result / with_nums[-1], with_nums[:-1])

def solve_part_1():
    total_possible = 0
    for res, nums in combos:
        if is_possible_1(res, nums):
            total_possible += res
    return total_possible

# Part 2

def is_possible_2(so_far, needs_result, nums_left):
    if len(nums_left) == 0:
        return so_far == needs_result
    return is_possible_2(so_far + nums_left[0], needs_result, nums_left[1:])\
        or is_possible_2(so_far * nums_left[0], needs_result, nums_left[1:])\
        or is_possible_2(int(str(so_far) + str(nums_left[0])), needs_result, nums_left[1:])

def solve_part_2():
    total_possible = 0
    for res, nums in combos:
        if is_possible_2(0, res, nums):
            total_possible += res
    return total_possible


submit_result_day(7, 1, solve_part_1)

submit_result_day(7, 2, solve_part_2())
