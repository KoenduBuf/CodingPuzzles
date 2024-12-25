from aoc_general import *




def get_inputs():
    all_inputs = read_input_day(25).split("\n\n")

    def count_hashtags_on_x(lines, x):
        return sum(1 for line in lines if line[x] == "#")
    
    def to_hashtag_count(lines):
        return tuple( count_hashtags_on_x(lines, x) for x in range(len(lines[0])) )

    block_heights, locks, keys = [], [], []
    for block in all_inputs:
        lines = block.split("\n")
        block_heights.append(len(lines))
        heights = to_hashtag_count(lines)
        if lines[0][0] == "#":
            keys.append(heights)
        else:
            locks.append(heights)
    
    if not all(block_heights[0] == bh for bh in block_heights):
        raise ValueError("All blocks should have the same height")

    return locks, keys, block_heights[0]


def solve_part_1():
    locks, keys, block_height = get_inputs()

    fitting_pairs = []
    for key in keys:
        for lock in locks:
            total = (a + b for a, b in zip(key, lock))
            if any(t > block_height for t in total):
                continue
            fitting_pairs.append((key, lock))
    
    return len(fitting_pairs)

submit_result_day(25, 1, solve_part_1())