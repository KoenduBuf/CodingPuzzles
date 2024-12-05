from aoc_general import *

data = read_input_day(5)

rules, updates = [ sec.split("\n") for sec in data.split("\n\n") ]

page_forbidden_rules_dict = {}
for rule in rules:
    parts = [ int(num) for num in rule.strip().split("|") ]
    page_forbidden_rules_dict.setdefault(parts[0], set()).add(parts[1])

def update_is_correct(update):
    had = set()
    for page in update:
        had.add(page)
        if page not in page_forbidden_rules_dict:
            continue
        for rule in page_forbidden_rules_dict[page]:
            if rule in had:
                return False
    return True

class PagesRulesComparator(int):
    def __lt__(self, other):
        if self in page_forbidden_rules_dict and other in page_forbidden_rules_dict[self]:
            return True
        # if other in page_forbidden_rules_dict and self in page_forbidden_rules_dict[other]:
        #     return 1
        return False

def solve_part_1():
    total_res = 0
    for update in updates:
        pages = [ int(page) for page in update.strip().split(",") ]
        if update_is_correct(pages):
            total_res += pages[len(pages) // 2]
    return total_res

def solve_part_2():
    total_res = 0
    for update in updates:
        pages = [ int(page) for page in update.strip().split(",") ]
        if update_is_correct(pages):
            continue
        sorted_pages = sorted(pages, key=PagesRulesComparator)
        if not update_is_correct(sorted_pages):
            raise KeyError("No correct update found")
        total_res += sorted_pages[len(sorted_pages) // 2]
    return total_res


submit_result_day(5, 1, solve_part_1)

submit_result_day(5, 2, solve_part_2)
