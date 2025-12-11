from aoc_general import *

input_data = read_input_day(2).strip()
range_tuples = [tuple(r.split("-")) for r in input_data.split(",")]

def is_invalid(c: str, max_times=10) -> bool:
    for repeats in range(2, max_times + 1):
        if len(c) % repeats == 0:
            segment_length = len(c) // repeats
            segment = c[:segment_length]
            if segment * repeats == c:
                return True
    return False

def invalids_in_range(start: int, end: int) -> list[int]:
    invalids = []
    for i in range(start, end + 1):
        if is_invalid(str(i)):
            print(f"Invalid code found: {i}")
            invalids.append(i)
    return invalids

# Part 1 & 2 (set max_times to 2 for part 1):

invalids_sum = 0
for r in range_tuples:
    start, end = int(r[0]), int(r[1])
    invalids_sum += sum(invalids_in_range(start, end))

submit_result_day(2, 2, invalids_sum)
