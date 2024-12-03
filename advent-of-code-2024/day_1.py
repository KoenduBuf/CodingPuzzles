from aoc_general import read_input_day

lines = read_input_day(1).split("\n")
nums = [ ln.split(" ") for ln in lines ]

nums_1 = sorted(int(num[0]) for num in nums)
nums_2 = sorted(int(num[1]) for num in nums)

# Part 1:

diffs = [ abs(a - b) for a, b in zip(nums_1, nums_2) ]
total_diffs = sum(diffs)

print(total_diffs)

# Part 2:

sim_scores = [ num * nums_2.count(num) for num in nums_1 ]
total_sim_scores = sum(sim_scores)

print(total_sim_scores)