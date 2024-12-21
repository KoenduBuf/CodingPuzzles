import re


class Keypad:
    def __init__(self, dict, gap):
        # A = (0, 0), Positive Y is up
        # Keypad (dx, dy, y_first)
        self.position_dict = dict
        self.gap = gap
    
    def to_key(self, from_key, to_key):
        from_x, from_y = self.position_dict[from_key]
        to_x, to_y = self.position_dict[to_key]
        return to_x - from_x, to_y - from_y

    def to_key_moves(self, from_key, to_key, y_first) -> str:
        dx, dy = self.to_key(from_key, to_key)
        mx = ("<" if dx < 0 else ">") * abs(dx)
        my = ("v" if dy < 0 else "^") * abs(dy)
        return my + mx if y_first else mx + my
    
    def can_move(self, from_key, to_key, y_first) -> bool:
        from_x, from_y = self.position_dict[from_key]
        to_x, to_y = self.position_dict[to_key]
        if y_first and from_x == self.gap[0] and to_y == self.gap[1]:
            return False
        if not y_first and from_y == self.gap[1] and to_x == self.gap[0]:
            return False
        return True
    
    def all_ways_to_key(self, from_key, to_key) -> list[str]:
        return list(set([
            self.to_key_moves(from_key, to_key, y)
            for y in (True, False)
            if self.can_move(from_key, to_key, y)
        ]))
    
    def all_ways_to_press_all_keys(self, from_key: str, keys: str):
        ways_to_check = [ (from_key, "") ]
        for key in keys:
            ways_to_this_key = []
            for at, moves in ways_to_check:
                ways_to_this_key.extend([
                    (key, moves + way + "A")
                    for way in self.all_ways_to_key(at, key)
                ])
            ways_to_check = ways_to_this_key
        return ways_to_check


class KeypadChain:
    def __init__(self, keypad: Keypad | list[Keypad], child_chain: "KeypadChain"=None):
        if isinstance(keypad, list):
            self.keypad = keypad[0]
            self.child_chain = KeypadChain(keypad[1:]) if len(keypad) > 1 else None
        else:
            self.keypad = keypad
            self.child_chain = child_chain
    
    def all_ways_to_press_final_keypad(self, keys):
        # For numeric keypad
        if self.child_chain is None:
            return self.keypad.all_ways_to_press_all_keys("A", keys)
        # For the arrows keypads
        all_child_ways = self.child_chain.all_ways_to_press_final_keypad(keys)
        all_ways_for_this_keypad: list[tuple[str, str]] = []
        for _, child_moves in all_child_ways:
            for this_way in self.keypad.all_ways_to_press_all_keys("A", child_moves):
                all_ways_for_this_keypad.append(this_way)
        return all_ways_for_this_keypad
        

keypad_numbers = Keypad({
    "A": ( 0, 0),
    "0": (-1, 0),
    "1": (-2, 1),
    "2": (-1, 1),
    "3": ( 0, 1),
    "4": (-2, 2),
    "5": (-1, 2),
    "6": ( 0, 2),
    "7": (-2, 3),
    "8": (-1, 3),
    "9": ( 0, 3),
}, (-2, 0))

keypad_arrows = Keypad({
    "A": ( 0,  0),
    "<": (-2, -1),
    ">": ( 0, -1),
    "^": (-1,  0),
    "v": (-1, -1),
}, (-2, 0))


from aoc_general import *


def get_keypad_chain(n_robots):
    return KeypadChain(
        [ keypad_arrows for _ in range(n_robots) ] +
        [ keypad_numbers ]
    )

def get_complexitys(keypad_chain, codes_to_press):
    final_ways_lenghts = []
    for code in codes_to_press:
        ways = keypad_chain.all_ways_to_press_final_keypad(code)
        ways_lengths = [ len(moves) for _, moves in ways ]
        final_ways_lenghts.append(min(ways_lengths))
    numberic_parts = [ int(re.sub(r"[^0-9]", "", code)) for code in codes_to_press ]
    complexitys = [ a * b for a, b, in zip(numberic_parts, final_ways_lenghts) ]
    return sum(complexitys)

def solve_part_1():
    keypad_chain = get_keypad_chain(2)
    codes_to_press = read_input_day(21).split("\n")
    return get_complexitys(keypad_chain, codes_to_press)

def solve_part_2():
    # keypad_chain = get_keypad_chain(25)
    codes_to_press = [ "029A" ] # read_input_day(21).split("\n")
    # return get_complexitys(keypad_chain, [ "029A" ])

    for code in codes_to_press:
        bottom_robot_directions_press = keypad_arrows.all_ways_to_press_all_keys("A", code)
        

submit_result_day(21, 1, solve_part_1())

# submit_result_day(21, 2, solve_part_2())

print(solve_part_2())
