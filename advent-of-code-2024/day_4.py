import numpy as np
from scipy import signal
from aoc_general import *

lines = read_input_day(4).split("\n")
data = [ [ ord(c) for c in line.strip() ] for line in lines if len(line) > 0 ]
matrix = np.array(data)

X = ord("X")
M = ord("M")
A = ord("A")
S = ord("S")

def count_masks(masks, for_values):
    to_find = sum([ ord(c) * ord(c) for c in for_values ])
    total_count = 0
    for mask in masks:
        res = signal.convolve2d(matrix, mask, mode="valid")
        count = np.sum(res == to_find)
        total_count += count
    return total_count

def solve_part_1():
    part_1_xmas_masks = [
        np.array([ [ X, M, A, S ] ]),
        np.array([ [ S, A, M, X ] ]),
        np.array([ [ X ], [ M ], [ A ], [ S ] ]),
        np.array([ [ S ], [ A ], [ M ], [ X ] ]),
        np.array([ [ X, 0, 0, 0 ], [ 0, M, 0, 0 ], [ 0, 0, A, 0 ], [ 0, 0, 0, S ] ]),
        np.array([ [ S, 0, 0, 0 ], [ 0, A, 0, 0 ], [ 0, 0, M, 0 ], [ 0, 0, 0, X ] ]),
        np.array([ [ 0, 0, 0, X ], [ 0, 0, M, 0 ], [ 0, A, 0, 0 ], [ S, 0, 0, 0 ] ]),
        np.array([ [ 0, 0, 0, S ], [ 0, 0, A, 0 ], [ 0, M, 0, 0 ], [ X, 0, 0, 0 ] ]),
    ]
    return count_masks(part_1_xmas_masks, "XMAS")

def solve_part_2():
    part_2_x_mas_masks = [
        np.array([ [ M, 0, M ], [ 0, A, 0 ], [ S, 0, S ] ]),
        np.array([ [ M, 0, S ], [ 0, A, 0 ], [ M, 0, S ] ]),
        np.array([ [ S, 0, S ], [ 0, A, 0 ], [ M, 0, M ] ]),
        np.array([ [ S, 0, M ], [ 0, A, 0 ], [ S, 0, M ] ]),
    ]
    return count_masks(part_2_x_mas_masks, "MMASS")

submit_result_day(4, 1, solve_part_1)

submit_result_day(4, 2, solve_part_2)

# time_solve(solve_part_2)
