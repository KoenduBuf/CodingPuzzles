from aoc_general import *

field_matrix = read_input_day(7).strip().split("\n")

beams = [ (field_matrix[0].index('S'), 0, 1) ]

splits_done = 0

def tick(beams: list[tuple[int, int]]) -> list[tuple[int, int]]:
    global splits_done
    new_beams = []
    for x, y, count in beams:
        if y + 1 >= len(field_matrix):
            continue
        below = field_matrix[y+1][x]
        if below == '^':
            splits_done += 1
            new_beams.append((x-1, y+1, count))
            new_beams.append((x+1, y+1, count))
        else:
            new_beams.append((x, y+1, count))

    # Merge beams, and count them
    beams_map = {}
    for nb in new_beams:
        if (nb[0], nb[1]) in beams_map:
            beams_map[(nb[0], nb[1])] += nb[2]
        else:
            beams_map[(nb[0], nb[1])] = nb[2]
    
    return [(k[0], k[1], v) for k, v in beams_map.items()]


while not all(b[1] == len(field_matrix) - 1 for b in beams):
    beams = tick(beams)

submit_result_day(7, 1, splits_done)

submit_result_day(7, 2, sum(b[2] for b in beams))
