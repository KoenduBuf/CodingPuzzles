from queue import PriorityQueue

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
    def __init__(self, data: str, width: int = None, height: int = None):
        if width is not None and height is not None:
            # Initialize grid with a given size
            fill_value = data if len(data) == 1 else None
            self.grid = [ [ fill_value for _ in range(width) ] for _ in range(height) ]
        else:
            # Initialize grid with a string, height = lines, width = line length
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

    def copy(self):
        new_grid = Grid("", width=len(self.grid[0]), height=len(self.grid))
        for pos in self:
            new_grid[pos] = self[pos]
        return new_grid

    def find(self, value: any) -> tuple[int, int]:
        for pos in self:
            if self[pos] == value:
                return pos
        return None
    
    def find_all(self, value: any) -> list[tuple[int, int]]:
        return [ pos for pos in self if self[pos] == value ]
    
    def path(self, start, goal):
        def possible_moves_func(cost, state):
            x, y = state
            for dx, dy in DIRECTIONS_4:
                new_x, new_y = x + dx, y + dy
                if (new_x, new_y) in self and self[(new_x, new_y)] != "#":
                    yield cost + 1, (new_x, new_y)
        # Start can be a position already or a char to find
        if isinstance(start, str):
            start = self.find(start)
        if not isinstance(start, tuple):
            raise ValueError("Start must be a tuple")
        result = self.dijkstra(start, goal, possible_moves_func)
        if result is None:
            return None
        cost, final_state, back_map = result
        path_to_goal = self.reconstruct_path(back_map, final_state)
        if len(path_to_goal) != cost + 1:
            raise Exception("Somethings wrong here")
        return path_to_goal

    def reconstruct_path(self, back_map, final_state):
        at_state = final_state
        path = [ at_state ]
        while at_state in back_map:
            _, ways = back_map[at_state]
            at_state = ways[0]
            path.append(at_state)
        manual = path[::-1]
        from_all = next(self.reconstruct_all_paths(back_map, final_state))
        if manual != from_all:
            raise Exception("Somethings wrong here")
        return manual

    def reconstruct_all_paths(self, back_map, final_state):
        paths_back_stack = [ [ final_state ] ]
        while len(paths_back_stack) > 0:
            path_back = paths_back_stack.pop()
            if path_back[-1] not in back_map:
                yield path_back[::-1]
                continue
            _, ways = back_map[path_back[-1]]
            for way in reversed(ways):
                paths_back_stack.append(path_back + [ way ])

    def dijkstra(self, initial_state, goal, possible_moves_func, longer_paths_too=False, show_progress=False):
        # Goal will be a set of positions
        if isinstance(goal, str):
            goal = set(self.find_all(goal))
        if isinstance(goal, tuple):
            goal = set([ goal ])
        if not isinstance(goal, set):
            raise ValueError("Goal must be a set of positions")

        # Setup for Dijkstra queue is (cost, state, previous_state)
        state = initial_state
        back_map = {}
        queue = PriorityQueue()
        queue.put((0, state, None))
        earliest_solution = None
        if show_progress:
            show_dijkstra_preamble = " >> Running Dijkstra... "
            print(show_dijkstra_preamble, end="")

        while not queue.empty():
            cost, state, prev_state = queue.get()
            if show_progress and len(back_map.keys()) % 10_000 == 0:
                print(f"\r{show_dijkstra_preamble} - Searched: {len(back_map.keys()):> 8} | Queued: {queue.qsize():> 8}", end="")

            # Create backmap and check if we have already visited this state
            if state in back_map:
                if back_map[state][0] > cost:
                    raise Exception("This should not happen")
                if back_map[state][0] == cost:
                    back_map[state][1].append(prev_state)
                continue
            if prev_state is not None:
                back_map[state] = (cost, [ prev_state ])

            # Check if we have reached the goal
            if not isinstance(state, tuple):
                raise ValueError("State must be a tuple")
            if state in goal or isinstance(state[0], tuple) and state[0] in goal:
                if earliest_solution is None:
                    earliest_solution = (cost, state)
                if not longer_paths_too:
                    break
            
            # Add all possible moves to the queue
            for new_cost, new_state in possible_moves_func(cost, state):
                if new_state != initial_state:
                    queue.put((new_cost, new_state, state))

        if show_progress:
            print(f"{show_dijkstra_preamble} - Finished. Searched {len(back_map.keys())} states.")
        return earliest_solution[0], earliest_solution[1], back_map
    