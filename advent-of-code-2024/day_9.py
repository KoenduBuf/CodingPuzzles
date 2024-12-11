from aoc_general import *
from queue import PriorityQueue

disk_nums_alternating = [ int(i) for i in read_input_day(9) ]

def checksum_from_layout(disk_layout):
    total = 0
    for i in range(len(disk_layout)):
        if disk_layout[i] == ".":
            continue
        total += (i * int(disk_layout[i]))
    return total

def alternating_to_layout(alternating):
    layout = [ ([ "." ] if i % 2 == 1 else [ str(i // 2) ]) * n for i, n in enumerate(alternating) ]
    layout = [ c for s in layout for c in s ]
    return layout

def move_compress_by_block(layout):
    to_move_to = PriorityQueue()
    for i in range(len(layout)):
        if layout[i] != ".":
            continue
        to_move_to.put(i)

    for i in reversed(range(len(layout))):
        if layout[i] == ".":
            continue
        to = to_move_to.get()
        if to >= i:
            break
        layout[to] = layout[i]
        layout[i] = "."
        to_move_to.put(i)
    
    return layout

def display_alternating_with_id(alternating_with_id):
    for id, size in alternating_with_id:
        print(("." if id == -1 else str(id)) * size, end="")
    print()

def move_compress_by_whole_file(alternating):
    alternating_with_id = [ (-1 if i % 2 == 1 else i // 2, n) for i, n in enumerate(alternating) ]
    original = [ n for n in alternating_with_id ]

    def find_spot(for_size):
        for i in range(1, len(alternating_with_id), 2):
            if alternating_with_id[i][1] >= for_size:
                return i
        return -1
    
    at_f_id = len(alternating_with_id) // 2
    at_pos = at_f_id * 2
    while at_pos > 0:
        id, size = alternating_with_id[at_pos]
        if size == 0 or id > at_f_id:
            at_pos -= 2
            continue
        to = find_spot(size)
        # display_alternating_with_id(alternating_with_id)
        # print(f"Moving {id} with size {size} from pos {at_pos} to {to} (len {len(alternating_with_id)})")
        if to == -1 or to >= at_pos:
            at_pos -= 2
            at_f_id -= 1
            continue
        spot_size = alternating_with_id[to][1]
        
        if to + 1 == at_pos:
            if to + 2 < len(alternating_with_id):
                alternating_with_id[to+2] = (-1, alternating_with_id[to][1] + alternating_with_id[to+2][1])
            alternating_with_id[to] = (-1, 0)
            at_pos -= 2
            at_f_id -= 1
            continue

        size_free_at_f_pos = size
        size_free_at_f_pos += alternating_with_id[at_pos-1][1]
        if at_pos < len(alternating_with_id) - 1:
            size_free_at_f_pos += alternating_with_id[at_pos+1][1]

        alternating_with_id[to+3:at_pos+1] = alternating_with_id[to+1:at_pos-1]
        alternating_with_id[to] = (-1, 0)
        alternating_with_id[to+1] = (id, size)

        if to < len(alternating_with_id) - 2:
            alternating_with_id[to+2] = (-1, spot_size - size)

        if at_pos < len(alternating_with_id) - 1:
            alternating_with_id[at_pos+1] = (-1, size_free_at_f_pos)
        at_f_id -= 1

    # 6311837662089 <- correct
    # 6311872499717

    # display_alternating_with_id(alternating_with_id)
    
    # total_disk_size_1 = sum([ n for n in alternating ])
    # total_disk_size_2 = sum([ n for i, n in alternating_with_id ])
    # if total_disk_size_1 != total_disk_size_2:
    #     print(original[:5], original[-5:], total_disk_size_1)
    #     print(alternating_with_id[:5], alternating_with_id[-5:], total_disk_size_2)
    #     raise Exception("Should have the same total disk size")

    # checksum
    total_checksum = 0
    at_pos = 0
    had_ids = {}
    for i in range(0, len(alternating_with_id)):
        if i % 2 == 1:
            at_pos += alternating_with_id[i][1]
            continue
        
        if alternating_with_id[i][0] in had_ids:
            print(f"Found id {alternating_with_id[i][0]} at pos {at_pos} and {had_ids[alternating_with_id[i][0]]}")
            raise Exception("Should not have any duplicate ids")
        had_ids[alternating_with_id[i][0]] = at_pos

        for _ in range(alternating_with_id[i][1]):
            if alternating_with_id[i][0] == -1:
                raise Exception("Should not have any -1s")
            # print(f"Adding {at_pos} * {alternating_with_id[i][0]}")
            total_checksum += at_pos * alternating_with_id[i][0]
            at_pos += 1

    if len(had_ids.keys()) != (1 + len(alternating) // 2):
        raise Exception("Should have all ids")
    
    return total_checksum

def solve_part_1():
    layout = alternating_to_layout(disk_nums_alternating)
    compressed = move_compress_by_block([ e for e in layout ])
    return checksum_from_layout(compressed)

def solve_part_2():
    return move_compress_by_whole_file([ e for e in disk_nums_alternating ])



submit_result_day(9, 1, solve_part_1)

submit_result_day(9, 2, solve_part_2)
