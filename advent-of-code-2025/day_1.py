from aoc_general import *


class SafeDial:
    def __init__(self):
        self.at = 50
        self.stop_at_zero = 0
        self.turns_by_zero = 0
    
    def process(self, inst):
        print(f"Processing instruction '{inst}' from position {self.at}")
        if inst[0] == "L":
            return self.turn(-int(inst[1:]))
        elif inst[0] == "R":
            return self.turn(int(inst[1:]))
        raise ValueError(f"Invalid instruction '{inst}'")

    def turn(self, steps):
        if self.at == 0:
            self.stop_at_zero += abs(steps) // 100
        else:
            self.turns_by_zero += abs(steps) // 100

        sign = 1 if steps >= 0 else -1
        steps = sign * (abs(steps) % 100)
        
        if steps != 0:
            started_at_zero = self.at == 0
            self.at += steps
            if self.at < 0:
                self.at += 100
                if not started_at_zero:
                    self.turns_by_zero += 1
            if self.at > 100:
                self.turns_by_zero += 1
            if self.at > 99:
                self.at -= 100

        if self.at == 0:
            self.stop_at_zero += 1
        return self.at
    

instructions = read_input_day(1).split("\n")

dial = SafeDial()

# Part 1:

for inst in instructions:
    dial.process(inst)

submit_result_day(1, 1, dial.stop_at_zero)

# Part 2:

submit_result_day(1, 2, dial.stop_at_zero + dial.turns_by_zero)
