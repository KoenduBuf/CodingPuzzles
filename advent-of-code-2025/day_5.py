from aoc_general import *

# Parse input
fresh_ranges, ingredients = read_input_day(5).strip().split("\n\n")

ingredients = [int(x) for x in ingredients.split("\n")]
fresh_ranges = [tuple(map(int, r.split("-"))) for r in fresh_ranges.split("\n")]

# Sort and merge ranges

fresh_ranges = sorted(fresh_ranges, key=lambda x: x[0])

merged_ranges = []
for r in fresh_ranges:
    if len(merged_ranges) == 0:
        merged_ranges.append(r)
    else:
        last_range = merged_ranges[-1]
        if r[0] <= last_range[1] + 1:
            merged_ranges[-1] = (last_range[0], max(last_range[1], r[1]))
        else:
            merged_ranges.append(r)

# Function to check if an ingredient is fresh

import bisect

def is_fresh(value: int) -> bool:
    idx = bisect.bisect_left(merged_ranges, (value, float('inf')))
    if idx == 0:
        return False
    possible_range = merged_ranges[idx-1]
    return possible_range[0] <= value <= possible_range[1]

# Part 1

fresh_ingredients = list(filter(is_fresh, ingredients))

submit_result_day(5, 1, len(fresh_ingredients))

# Part 2

range_sizes = [r[1] - r[0] + 1 for r in merged_ranges]
total_fresh_capacity = sum(range_sizes)

submit_result_day(5, 2, total_fresh_capacity)
