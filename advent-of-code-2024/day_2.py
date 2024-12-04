from aoc_general import *

lines = read_input_day(2).split("\n")

correct = 0

for ln in lines:
    nums = [ int(n) for n in ln.split(" ") ]

    for skip in range(len(nums)):

        use_nums = nums[:skip] + nums[skip+1:]
        diffs = [ a - b for a, b in zip(use_nums, use_nums[1:]) ]
        if not all([ abs(d) >= 1 and abs(d) <= 3 for d in diffs ]):
            continue
        if not all([ d > 0 for d in diffs ]) and not all([ d < 0 for d in diffs ]):
            continue

        correct += 1
        break
    
submit_result_day(1, 2, correct)