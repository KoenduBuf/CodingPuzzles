from aoc_general import *

grid = read_input_day(4).strip().split("\n")

def iter_around(x: int, y: int) -> int:
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
                yield grid[ny][nx]

def rolls_around(x: int, y: int) -> int:
    total = 0
    for value in iter_around(x, y):
        if value == '@':
            total += 1
    return total


def is_accessible(x: int, y: int) -> bool:
    if grid[y][x] != '@':
        return False
    return rolls_around(x, y) < 4

def remove_accessible_rolls():
    accessible_positions = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if is_accessible(x, y):
                accessible_positions.append((x, y))
    for (x, y) in accessible_positions:
        grid[y] = grid[y][:x] + '.' + grid[y][x+1:]
    return len(accessible_positions)


total_rolls = sum(row.count('@') for row in grid)

submit_result_day(4, 1, remove_accessible_rolls())

while remove_accessible_rolls() > 0:
    pass

remainin_rolls = sum(row.count('@') for row in grid)

submit_result_day(4, 2, total_rolls - remainin_rolls)
