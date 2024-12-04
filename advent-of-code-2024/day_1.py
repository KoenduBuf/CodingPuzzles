from aoc_general import *

lines = read_input_day(1).split("\n")
nums = [ ln.split(" ") for ln in lines ]

nums_1 = sorted(int(num[0]) for num in nums)
nums_2 = sorted(int(num[1]) for num in nums)

# Part 1:

diffs = [ abs(a - b) for a, b in zip(nums_1, nums_2) ]
total_diffs = sum(diffs)

submit_result_day(1, 1, total_diffs)

# Part 2:

sim_scores = [ num * nums_2.count(num) for num in nums_1 ]
total_sim_scores = sum(sim_scores)

submit_result_day(1, 2, total_sim_scores)