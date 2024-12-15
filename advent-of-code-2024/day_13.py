from aoc_general import *
import math

SIGMA = 0.001

class Machine:
    def __init__(self, text):
        lines = text.split("\n")
        if not lines[0].startswith("Button A:") or not len(lines) == 3:
            raise ValueError("Invalid machine text")
        self.dA = tuple(int(n[2:]) for n in lines[0].split(": ")[1].split(", "))
        self.dB = tuple(int(n[2:]) for n in lines[1].split(": ")[1].split(", "))
        self.goal = tuple(int(n[2:]) for n in lines[2].split(": ")[1].split(", "))
        self.moves = [ (3, self.dA), (1, self.dB) ]
    
    def __str__(self):
        return f"Machine({self.dA}, {self.dB}, {self.goal})"
    
    def __repr__(self):
        return str(self)
    
    def solve(self):
        return self.least_cost_quick_maths(self.moves, self.goal)

    def check_if_possible(self, a_count, b_count):
        at_x = self.dA[0] * a_count + self.dB[0] * b_count
        at_y = self.dA[1] * a_count + self.dB[1] * b_count
        if at_x == self.goal[0] and at_y == self.goal[1]:
            return a_count * self.moves[0][0] + b_count * self.moves[1][0]
        return float("inf")

    def least_cost_to_goal_brute_force(self, moves, goal):
        # No moves or no goal, we are done
        if goal == (0, 0):
            return 0
        if goal[0] < 0 or goal[1] < 0:
            return float("inf")
        if len(moves) == 0:
            return float("inf")
        
        # Only 1 move: check if it is possible to reach the goal
        this_move_cost, this_move = moves[0]
        if len(moves) == 1:
            if goal[0] % this_move[0] != 0 or goal[1] % this_move[1] != 0:
                return float("inf")
            if goal[0] // this_move[0] != goal[1] // this_move[1]:
                return float("inf")
            return this_move_cost * (goal[0] // this_move[0])

        # More than 1 move: try all possible combinations
        best_cost = float("inf")
        can_do_at_most = min(goal[0] // this_move[0] + 2, goal[1] // this_move[1] + 2)
        for do_i_times in range(can_do_at_most):
            left = (goal[0] - do_i_times * this_move[0], goal[1] - do_i_times * this_move[1])
            least_with_rest = self.least_cost_to_goal_brute_force(moves[1:], left)
            if least_with_rest == float("inf"):
                continue
            best_cost = min(best_cost, do_i_times * this_move_cost + least_with_rest)
        return best_cost

    def least_cost_quick_maths(self, moves, goal):
        # Calculate how much each move would move us away from the center line towards to goal
        moves_len = [ math.sqrt(m[1][0] ** 2 + m[1][1] ** 2) for m in moves ]
        goal_angle = math.atan(goal[1] / goal[0])
        move_angles = [ math.atan(d[1] / d[0]) for _, d in moves ]
        move_angle_diffs = [ goal_angle - ma for ma in move_angles ]
        move_distance_from_center = [ math.sin(ma) * ml for ma, ml in zip(move_angle_diffs, moves_len) ]

        # If one of the moves is exactly towards the goal, we are done one way or another
        if any(abs(m) < SIGMA for m in move_distance_from_center):
            if all(abs(m) < SIGMA for m in move_distance_from_center):
                # If both are, find the cheapest way to the goal
                raise NotImplementedError("Not implemented")
            # If only one is, we can calculate the cost
            move_to_goal_idx = 0 if abs(move_distance_from_center[0]) < SIGMA else 1
            need_x = goal[0] / moves[move_to_goal_idx][1][0]
            need_y = goal[1] / moves[move_to_goal_idx][1][1]
            if abs(need_x - need_y) > SIGMA:
                return float("inf")
            if abs(need_x - round(need_x)) > SIGMA:
                return float("inf")
            if move_to_goal_idx == 0:
                return self.check_if_possible(round(need_x), 0)
            return self.check_if_possible(0, round(need_x))
        
        # From this we can calculate the ratio of how much we need of each move
        move_distance_from_center_ratio = -move_distance_from_center[0] / move_distance_from_center[1]
        if move_distance_from_center_ratio < 0:
            return float("inf")
        
        # With that we can calculate how much we need of one of the moves
        single_move_by_ratio = (
            moves[0][1][0] + move_distance_from_center_ratio * moves[1][1][0],
            moves[0][1][1] + move_distance_from_center_ratio * moves[1][1][1]
        )
        need_a_x = goal[0] / single_move_by_ratio[0]
        need_a_y = goal[1] / single_move_by_ratio[1]
        if abs(need_a_x - need_a_y) > SIGMA:
            return float("inf")
        if abs(need_a_x - round(need_a_x)) > SIGMA:
            return float("inf")
        
        # If that is possible, we calculate the amount of the other move
        need_b_x = move_distance_from_center_ratio * need_a_x
        need_b_y = move_distance_from_center_ratio * need_a_y
        if abs(need_b_x - need_b_y) > SIGMA:
            return float("inf")
        if abs(need_b_x - round(need_b_x)) > SIGMA:
            return float("inf")

        # If all that is possible, calculate the cost
        return self.check_if_possible(round(need_a_x), round(need_b_x))


machines = [ Machine(chunk) for chunk in read_input_day(13).split("\n\n") ]

# Part 1:

best_costs = [ machine.solve() for machine in machines ]
submit_result_day(13, 1, sum(c for c in best_costs if c != float("inf")))


# Part 2:

for machine in machines:
    machine.goal = (machine.goal[0] + 10000000000000, machine.goal[1] + 10000000000000)

best_costs = [ machine.solve() for machine in machines ]
submit_result_day(13, 2, sum(c for c in best_costs if c != float("inf")))
