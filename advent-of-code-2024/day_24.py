from aoc_general import *

# Single gates

class Gate:
    def __init__(self, inputs, output):
        self.inputs = inputs
        self.output = output
    
    def check_perform(self, wire_values):
        if self.output in wire_values:
            return None
        if not all(input in wire_values for input in self.inputs):
            return None
        input_values = [wire_values[input] for input in self.inputs]
        return self.perform(*input_values)
    
    def __str__(self):
        return f"{type(self).__name__}({self.inputs}) -> {self.output}"
    
    def __repr__(self):
        return str(self)
    
    def perform(self, *input_values):
        raise NotImplementedError()

class AndGate(Gate):
    def perform(self, a, b):
        return a & b

class OrGate(Gate):
    def perform(self, a, b):
        return a | b

class XorGate(Gate):
    def perform(self, a, b):
        return a ^ b

type_map = {
    "AND": AndGate,
    "OR": OrGate,
    "XOR": XorGate,
}

# Gate chain

class GateRunner:
    def __init__(self, gates, wire_values):
        self.gates = gates
        self.wire_values = wire_values
        self.notify_map = {}
        for gate in gates:
            for input in gate.inputs:
                self.notify_map.setdefault(input, []).append(gate)
    
    def run(self):
        to_check = sum([
            self.notify_map[wire]
            for wire in self.wire_values
            if wire in self.notify_map ],
        [])

        while len(to_check) > 0:
            gate: Gate = to_check.pop(0)
            output = gate.check_perform(self.wire_values)
            if output is not None:
                self.wire_values[gate.output] = output
                if gate.output in self.notify_map:
                    to_check.extend(self.notify_map[gate.output])

# Part 1:

def read_input():
    set_values, gates_strs = read_input_day(24).split("\n\n")

    preset_wire_values = {}
    for set_value in set_values.split("\n"):
        wire, value = set_value.split(": ")
        preset_wire_values[wire] = int(value)

    all_gates = []
    for gate_str in gates_strs.split("\n"):
        gate, output = gate_str.split(" -> ")
        input_1, gate_type, input_2 = gate.split(" ")
        gate = type_map[gate_type](inputs=[input_1, input_2], output=output)
        all_gates.append(gate)
    
    return GateRunner(all_gates, preset_wire_values)

def get_z_outputs(gate_runner):
    z_gates = [ gate for gate in gate_runner.wire_values if gate.startswith("z") ]
    sorted_z_gates = sorted(z_gates, key=lambda x: int(x[1:]))
    values = [ gate_runner.wire_values[gate] for gate in sorted_z_gates ]
    output_int = 0
    for i, value in enumerate(values):
        output_int += (value << i)
    return output_int

def solve_part_1():
    gate_runner = read_input()
    gate_runner.run()
    return get_z_outputs(gate_runner)

# Part 2:

class Gates:
    def __init__(self):
        self.gates_list: list[Gate] = read_input().gates
        self.calculate_lookup_dicts()

    def calculate_lookup_dicts(self):
        gates_by_output = { gate.output: gate for gate in self.gates_list }
        gates_by_input = {}
        for gate in self.gates_list:
            for input in gate.inputs:
                gates_by_input.setdefault(input, []).append(gate)
        self.gates_by_output, self.gates_by_input = gates_by_output, gates_by_input
    
    def get_common_gates_with_inputs(self, with_inputs):
        common_gates = []
        for gate in self.gates_list:
            if all(input in with_inputs for input in gate.inputs):
                common_gates.append(gate)
        return sorted(common_gates, key=lambda g: type(g).__name__)
    
    def perform_swap(self, wire_a, wire_b):
        print(f"SWAPPING {wire_a} and {wire_b}")
        gate_a = self.gates_by_output[wire_a]
        gate_b = self.gates_by_output[wire_b]
        gate_a.output = wire_b
        gate_b.output = wire_a
        # for in_a in self.gates_by_input[wire_a]:
        #     in_a.inputs[in_a.inputs.index(wire_a)] = wire_b
        # for in_b in self.gates_by_input[wire_b]:
        #     in_b.inputs[in_b.inputs.index(wire_b)] = wire_a
        self.calculate_lookup_dicts()

    def __iter__(self):
        return iter(self.gates_list)

def solve_part_2():
    # I am gonna assume they all need to make half/full adders
    gates = Gates()
    
    # We are gonna track all gates that possibly need to change
    wires_to_change = set()

    # Helper functions
    def assert_or_change(cond, wire):
        if cond: return
        print(f"Changing {wire}")
        wires_to_change.add(wire)

    def assert_or_exception(cond, msg):
        if not cond: raise Exception(msg)

    # Get all z gates, and all x and y wires
    sort_wires = lambda x: sorted(x, key=lambda x: int(x.output[1:]) if isinstance(x, Gate) else int(x[1:]))
    z_gates = sort_wires([ g for g in gates if g.output[0] == "z" ])
    x_wires = sort_wires(list(set([ inp for g in gates for inp in g.inputs if inp[0] == "x" ])))
    y_wires = sort_wires(list(set([ inp for g in gates for inp in g.inputs if inp[0] == "y" ])))
    assert_or_exception(len(x_wires) == len(y_wires), "Not the same amount of x and y wires")


    # First, check that x00 and y00 make a half adder
    gates_from_00 = gates.get_common_gates_with_inputs(["x00", "y00"])
    assert_or_exception(len(gates_from_00) == 2, "x00 and y00 should have 2 gates")
    assert_or_exception(isinstance(gates_from_00[0], AndGate), "x00 and y00 should have an and")
    assert_or_exception(isinstance(gates_from_00[1], XorGate), "y00 and y00 should have an xor")

    assert_or_change(gates_from_00[1].output == "z00", "z00 should be the output of the first xor")
    carry_00 = gates_from_00[0].output
    previous_carry = carry_00

    # Then we go over all the full adders
    for x_wire, y_wire in zip(x_wires[1:], y_wires[1:]):
        this_z_wire = f"z{x_wire[1:]}"
        print(f"Checking full adder from {x_wire}, {y_wire}, {previous_carry} -> {this_z_wire}")
        common_gates = gates.get_common_gates_with_inputs([x_wire, y_wire])

        # We assume the full adder design uses 2 half adders in the common way (please dont make me reget this)
        assert_or_exception(len(common_gates) == 2, "any x and y should have 2 gates")
        assert_or_exception(isinstance(common_gates[0], AndGate), "any x and y should have an and")
        assert_or_exception(isinstance(common_gates[1], XorGate), "any x and y should have an xor")

        a_and_y = common_gates[0].output
        a_xor_y = common_gates[1].output

        # After the xor there should be another xor with the carry
        gates_after_xor = gates.get_common_gates_with_inputs([a_xor_y, previous_carry])
        if len(gates_after_xor) != 2:
            a = gates.gates_by_input[a_xor_y]
            b = gates.gates_by_input[previous_carry]

            if len(b) == 2:
                not_carry_wires = [ inp for g in b for inp in g.inputs if inp != previous_carry ]
                unique_wire = list(set(not_carry_wires))
                assert_or_exception(len(unique_wire) == 1, "There should be only one unique wire")
                gates.perform_swap(previous_carry, unique_wire[0])
                a_xor_y = unique_wire[0]
                gates_after_xor = gates.get_common_gates_with_inputs([a_xor_y, previous_carry])

        assert_or_exception(len(gates_after_xor) == 2, "After xor there should be 2 gates")
        assert_or_exception(isinstance(gates_after_xor[0], AndGate), "After xor there should be an and")
        assert_or_exception(isinstance(gates_after_xor[1], XorGate), "After xor there should be an xor")
        
        assert_or_change(gates_after_xor[1].output == this_z_wire, f"The output of the xor should be {this_z_wire}")

        and_gate_after_xor = gates_after_xor[0]
        after_ands = gates.get_common_gates_with_inputs([a_and_y, and_gate_after_xor.output])
        if len(after_ands) != 1:
            a = gates.gates_by_input[a_and_y]
            b = gates.gates_by_input[gates_after_xor[0].output]
            print(a, b, after_ands)
        assert_or_exception(len(after_ands) == 1, "After the ands there should be 1 gate")
        assert_or_exception(isinstance(after_ands[0], OrGate), "After the ands there should be an or")

        previous_carry = after_ands[0].output

    
        


    



# submit_result_day(24, 1, solve_part_1())

print(solve_part_2())

