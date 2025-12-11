from aoc_general import *

input_data = read_input_day(6).strip().split("\n")
matrix = [line.strip().split(" ") for line in input_data]
matrix_t = list(zip(*matrix))

def prod(values: list[int]) -> int:
    total = 1
    for v in values:
        total *= v
    return total

def solve_line(line: tuple[str]) -> int:
    if line[-1] == '+':
        return sum(int(x) for x in line[:-1])
    elif line[-1] == '*':
        return prod([int(x) for x in line[:-1]])
    raise ValueError("Unknown operation")

# Part 1

total = 0
for line in matrix_t:
    total += solve_line(line)

submit_result_day(6, 1, total)

# Part 2

input_data = read_input_day(6, False).strip().split("\n")

max_line_len = len(max(input_data, key=len))
all_problem_results = []
current_problem_numbers = []
current_operation = None
for i in range(max_line_len):
    at_col = max_line_len - 1 - i
    
    # Get number in this column
    col_values = []
    for row in input_data:
        if at_col < len(row) and row[at_col].isdigit():
            col_values.append(row[at_col])
    if len(col_values) > 0:
        col_num = int("".join(col_values))
        current_problem_numbers.append(col_num)

    # If applicable, set operation
    funcs = { '+': sum, '*': prod }
    if len(input_data[-1]) > at_col and input_data[-1][at_col] in funcs:
        current_operation = funcs[input_data[-1][at_col]]
    
    # If no number at all, perform operation
    if len(col_values) == 0 or at_col == 0:
        if current_operation is None:
            raise ValueError("No operation set")
        result = current_operation(current_problem_numbers)
        current_problem_numbers = []
        current_operation = None
        all_problem_results.append(result)


submit_result_day(6, 2, sum(all_problem_results))
