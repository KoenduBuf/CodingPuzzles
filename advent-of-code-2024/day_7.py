from aoc_general import *

SIGMA = 0.00000000001

lines = read_input_day(7).split("\n")
combos = [ ( int(line.split(": ")[0]), [ int(n) for n in line.split(": ")[1].split(" ") ]) for line in lines ]

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

def is_possible_2(result, with_nums):
    if len(with_nums) == 1:
        return abs(with_nums[0] - result) < SIGMA
    
    if abs(int(result) - result) < SIGMA and str(result).endswith(str(with_nums[-1])):
        new_res = str(result)[:-len(str(with_nums[-1]))]
        if len(new_res) == 0:
            if is_possible_2(1, with_nums[:-1]) or is_possible_2(0, with_nums[:-1]):
                return True
        elif is_possible_2(int(new_res), with_nums[:-1]):
            return True
        
    return is_possible_2(result - with_nums[-1], with_nums[:-1]) or is_possible_2(result / with_nums[-1], with_nums[:-1])

def solve_part_2():
    total_possible = 0
    for res, nums in combos:
        if is_possible_2(res, nums):
            total_possible += res
    return total_possible


print(solve_part_2())

# submit_result_day(7, 1, solve_part_1)

# submit_result_day(7, 2, solve_part_2())
    