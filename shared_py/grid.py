
DIRECTIONS_4 = [
    (0, -1),    # Up
    (1, 0),     # Right
    (0, 1),     # Down
    (-1, 0),    # Left
]

DIRECTION_CHARS_4 = "^>v<"

def to_directions(directions: str) -> list[int]:
    return [ DIRECTION_CHARS_4.index(d) for d in directions if d in DIRECTION_CHARS_4 ]

def move(pos: tuple[int, int], direction: int) -> tuple[int, int]:
    return pos[0] + DIRECTIONS_4[direction][0], pos[1] + DIRECTIONS_4[direction][1]

def manhattan(pos1: tuple[int, int], pos2: tuple[int, int]) -> int:
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

class Grid:
    def __init__(self, data: str):
        self.grid = [ list(row) for row in data.split("\n") ]

    def __getitem__(self, pos: tuple[int, int]) -> any:
        return self.grid[pos[1]][pos[0]]

    def __setitem__(self, pos: tuple[int, int], value: any):
        self.grid[pos[1]][pos[0]] = value

    def __str__(self) -> str:
        return "\n".join("".join(str(self[(x, y)]) for x in range(len(self.grid[y]))) for y in range(len(self.grid)))

    def __repr__(self) -> str:
        return str(self)

    def __iter__(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                yield (x, y)

    def __contains__(self, pos: tuple[int, int]) -> bool:
        return 0 <= pos[1] < len(self.grid) and 0 <= pos[0] < len(self.grid[pos[1]])

    def find(self, value: any) -> tuple[int, int]:
        for pos in self:
            if self[pos] == value:
                return pos
        return None
    
    def find_all(self, value: any) -> list[tuple[int, int]]:
        return [ pos for pos in self if self[pos] == value ]