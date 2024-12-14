from aoc_general import *

DIRECTIONS = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0),
]

region = read_input_day(12).split("\n")


def fill_from(region, x, y):
    plant = region[y][x]
    stack = [(x, y)]
    been = set()
    while len(stack) > 0:
        at_x, at_y = stack.pop()

        if (at_x, at_y) in been:
            continue
        been.add((at_x, at_y))
        yield at_x, at_y

        for dx, dy in DIRECTIONS:
            nx, ny = at_x + dx, at_y + dy
            if nx < 0 or nx >= len(region[at_y]) or ny < 0 or ny >= len(region):
                continue
            if region[ny][nx] != plant:
                continue
            stack.append((nx, ny))

def plant_most_in_direction(region, from_x, from_y, dx, dy, other_dx, other_dy):
    x, y = from_x, from_y
    while True:
        nx, ny = x + dx, y + dy
        ox, oy = nx + other_dx, ny + other_dy
        if oy >= 0 and oy < len(region) and ox >= 0 and ox < len(region[oy]) and region[oy][ox] == region[ny][nx]:
            return (x, y)
        if nx < 0 or nx >= len(region[y]) or ny < 0 or ny >= len(region):
            return (x, y)
        if region[ny][nx] != region[y][x]:
            return (x, y)
        x, y = nx, ny

def solve_parts_1_and_2(part_2):
    total = 0
    been_to = set()

    for y in range(len(region)):
        for x in range(len(region[y])):
            
            if (x, y) in been_to:
                continue
            
            group_fence = 0
            group_plants = 0
            group_sides = set()
            plant = region[y][x]

            for px, py in fill_from(region, x, y):
                if (px, py) in been_to:
                    continue
                been_to.add((px, py))
                group_plants += 1

                for dx, dy in DIRECTIONS:
                    nx, ny = px + dx, py + dy

                    # Always a fence if out of bounds, or fence if different plant
                    if nx < 0 or nx >= len(region[y]) or ny < 0 or ny >= len(region) or region[ny][nx] != plant:
                        if dx == 0:
                            fx, fy = plant_most_in_direction(region, px, py, -1, 0, dx, dy)
                            group_sides.add(('h', fx + max(0, dx), fy + max(0, dy)))
                        if dy == 0:
                            fx, fy = plant_most_in_direction(region, px, py, 0, -1, dx, dy)
                            group_sides.add(('v', fx + max(0, dx), fy + max(0, dy)))
                        group_fence += 1
                        continue
            
            if not part_2:
                total += group_plants * group_fence
            else:
                total += group_plants * len(group_sides)


    # total_fence = 0
    # for group in fence_per_group.keys():
    #     print(f"Group of plants {region[group[1]][group[0]]} at {group} has {plants_per_group[group]} plants and {fence_per_group[group]} fences. {plants_per_group[group]} * {fence_per_group[group]} = {plants_per_group[group] * fence_per_group[group]}")
    #     total_fence += fence_per_group[group] * plants_per_group[group]

    return total

submit_result_day(12, 1, lambda: solve_parts_1_and_2(False))

submit_result_day(12, 2, lambda: solve_parts_1_and_2(True))
