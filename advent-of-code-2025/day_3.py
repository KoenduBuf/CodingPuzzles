from aoc_general import *

banks = read_input_day(3).strip().split("\n")

total_joltage = 0

def turn_on(bank: str, amount: int) -> int:
    last_on_index = -1
    got_digits = []
    for turn_on in range(amount):
        find_until = len(bank) - amount + turn_on + 1
        find_section = bank[last_on_index+1:find_until]
        this_on = max([int(x) for x in find_section])
        last_on_index = last_on_index + 1 + find_section.index(str(this_on))
        got_digits.append(str(this_on))
    return int("".join(got_digits))

# Part 1 & 2 (set amount to 2 for part 1):

for bank in banks:
    if len(bank) == 0:
        continue
    
    total_joltage += turn_on(bank, 12)

submit_result_day(3, 2, total_joltage)
