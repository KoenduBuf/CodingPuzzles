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
    
    def manhattan_distance(self, from_key, to_key):
        dx, dy = self.to_key(from_key, to_key)
        return abs(dx) + abs(dy)

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

    def fastest_way_to_press_all_keys(self, from_key: str, keys: str):
        all_ways = self.all_ways_to_press_all_keys(from_key, keys)
        return min(all_ways, key=lambda x: (len(x[1]), x[1]))[1]

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

def get_complexitys(way_lenghts, codes_to_press):
    numberic_parts = [ int(re.sub(r"[^0-9]", "", code)) for code in codes_to_press ]
    complexitys = [ a * b for a, b, in zip(numberic_parts, way_lenghts) ]
    return sum(complexitys)

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


# Part 1:

def get_way_lengths_try_all(keypad_chain: KeypadChain, codes_to_press):
    final_ways_lenghts = []
    for code in codes_to_press:
        ways = keypad_chain.all_ways_to_press_final_keypad(code)
        ways_lengths = [ len(moves) for _, moves in ways ]
        final_ways_lenghts.append(min(ways_lengths))
    return final_ways_lenghts

def solve_part_1():
    keypad_chain = KeypadChain(
        [ keypad_arrows for _ in range(2) ] +
        [ keypad_numbers ]
    )
    codes_to_press = read_input_day(21).split("\n")
    way_lengths = get_way_lengths_try_all(keypad_chain, codes_to_press)
    return get_complexitys(way_lengths, codes_to_press)

# Part 2, lookup table:

get_a_parts = lambda moves: [ m + "A" for m in moves.split("A")[:-1] ]

def get_all_possible_moves_with_a(depth=5):
    # All possible combinations of moves you could do before pressing A on an arrow keypad
    all_single_moves = [ "<", ">", "^", "v", "" ]
    def get_all_moves_of_length(n) -> list[str]:
        if n == 1:
            return all_single_moves
        return [ 
            move + way
            for way in get_all_moves_of_length(n - 1)
            for move in all_single_moves
        ]
    return [ mvs + "A" for mvs in get_all_moves_of_length(depth) ]

def build_length_lookup_table_bottom_up(for_depth):
    first_table, second_table = for_depth // 2 - 1, for_depth - 1 - for_depth // 2
    all_unique_moves_with_a = get_all_possible_moves_with_a()
    
    # For each of those, find the shortest way to do that move and then press A
    moves_1_depth_lookup = {
        move: keypad_arrows.fastest_way_to_press_all_keys("A", move)
        for move in all_unique_moves_with_a
    }

    # From now on, moves consists of moves between multiple A's, like xxxAxxAxxxxAxxAAxA
    # So we need to check the shortest way doing all of those parts between the As
    def fastest_way_for_all_parts(moves):
        return "".join(moves_1_depth_lookup[part] for part in get_a_parts(moves))

    # Now we can make a lookup table for lets say depth 13
    lookup_tables = [ moves_1_depth_lookup ]
    for i in range(1, second_table + 1):
        print("Making lookup table for depth", i)
        previous_table = lookup_tables[i - 1]
        depth_i_table = {
            move: fastest_way_for_all_parts(previous_table[move])
            for move in all_unique_moves_with_a
        }
        lookup_tables.append(depth_i_table)

    # Then we can make a lookup table of the length for depth 25 by going over the one
    # for depth 12 and for each move looking up the length in depth 13
    def total_length_to_move_all_parts(moves, with_table):
        return sum(len(with_table[part]) for part in get_a_parts(moves))
    
    depth_25_lengths = {
        move: total_length_to_move_all_parts(
            lookup_tables[first_table][move],
            lookup_tables[second_table]
        )
        for move in all_unique_moves_with_a
    }
    return depth_25_lengths

# Part 2, top down:

def build_length_lookup_table_top_down(for_depth):
    # New idea.
    all_unique_moves_with_a = get_all_possible_moves_with_a()

    # Lets start at robot 25. For each possible move of robot 24, how long does it take?
    takes_time_for_24 = {
        move: len(keypad_arrows.fastest_way_to_press_all_keys("A", move))
        for move in all_unique_moves_with_a
    }

    # When we know that, then how long for robot 23? Etc
    previous_takes_time_dict = takes_time_for_24
    for _ in range(for_depth - 1):
        takes_time_for_this_robot = {}

        for move in all_unique_moves_with_a:
            best_takes_time = float("inf")
            for _, way in keypad_arrows.all_ways_to_press_all_keys("A", move):
                way_takes = sum([ previous_takes_time_dict[part] for part in get_a_parts(way) ])
                if way_takes < best_takes_time:
                    best_takes_time = way_takes
            takes_time_for_this_robot[move] = best_takes_time
        
        previous_takes_time_dict = takes_time_for_this_robot
    
    return takes_time_for_this_robot

def solve_part_2_lookup_table(lookup_lengths_table):
    codes_to_press = read_input_day(21).split("\n")

    # Then lets do it on the actual code
    best_way_lengths = []
    for code in codes_to_press:
        first_bot_ways = keypad_numbers.all_ways_to_press_all_keys("A", code)
        best_way = float("inf")
        for _, arrow_ways in first_bot_ways:
            # For each way the first bot can do it, calculate the length N deep
            parts = get_a_parts(arrow_ways)
            parts_lengths = [ lookup_lengths_table[part] for part in parts ]
            if sum(parts_lengths) < best_way:
                best_way = sum(parts_lengths)
        best_way_lengths.append(best_way)
    
    return get_complexitys(best_way_lengths, codes_to_press)


submit_result_day(21, 1, solve_part_1())

submit_result_day(21, 2, solve_part_2_lookup_table(build_length_lookup_table_top_down(25)))
