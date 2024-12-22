from aoc_general import *

class MoneyPriceGenerator:
    def __init__(self, initial_number):
        self.initial_number = initial_number
        self.last_number = initial_number
    
    def next_number(self):
        s = self.last_number
        s = (s ^ (s << 6)) % 16777216
        s = (s ^ (s >> 5)) % 16777216
        s = (s ^ (s << 11)) % 16777216
        self.last_number = s
        return s
    
    def get_number(self, n):
        for _ in range(n):
            self.next_number()
        return self.last_number

    def get_every_4_changes(self):
        prev = self.last_number % 10
        last_changes = [ ]
        for _ in range(2000):
            n = self.next_number() % 10
            change = n - prev
            prev = n
            last_changes.append(change)
            if len(last_changes) > 4:
                last_changes.pop(0)
            if len(last_changes) == 4:
                yield last_changes, n





def solve_part_1():
    buyer_start_numbers = [ int(n) for n in read_input_day(22).split("\n")]
    buyer_generators = [ MoneyPriceGenerator(n) for n in buyer_start_numbers ]
    final_nums = [ g.get_number(2000) for g in buyer_generators ]
    return sum(final_nums)


def solve_part_2():
    buyer_start_numbers = [ int(n) for n in read_input_day(22).split("\n")]
    big_dict = { }

    for start_number in buyer_start_numbers:
        g = MoneyPriceGenerator(start_number)

        this_buyer = { }
        for changes, n in g.get_every_4_changes():
            if tuple(changes) not in this_buyer:
                this_buyer[tuple(changes)] = n

        for k, v in this_buyer.items():
            big_dict.setdefault(k, 0)
            big_dict[k] += v

    best_key = max(big_dict.keys(), key=lambda k: big_dict[k])
    return big_dict[best_key]


submit_result_day(22, 1, solve_part_1())

submit_result_day(22, 2, solve_part_2())
