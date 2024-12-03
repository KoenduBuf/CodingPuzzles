import re

def read_input_day(day):
    with open(f"./inputs/day_{day}.txt") as fd:
        return re.sub(r"[\t ]+", " ", fd.read().strip())
