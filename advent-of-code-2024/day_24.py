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

def solve_part_2():
    # I am gonna assume they all need to make half/full adders
    gates = read_input().gates

    # Easy lookup dicts
    gates_by_output = { gate.output: gate for gate in gates }
    gates_by_input = {}
    for gate in gates:
        for input in gate.inputs:
            gates_by_input.setdefault(input, []).append(gate)

    z_gates = sorted([ g for g in gates if g[0] == "z" ], key=lambda x: int(x.output[1:]))
    

    # Helper functions
    def get_common_gates_with_inputs(with_inputs):
        gates = []
        for gate in gates:
            if all(input in with_inputs for input in gate.inputs):
                gates.append(gate)
        return gates

    
    # We are gonna track all gates that possibly need to change
    wires_to_change = set()

    # First, check that all z gates are xors, except the last one
    for z_gate in z_gates[:-1]:
        if not isinstance(z_gate, XorGate):
            print("Nope Found, not xor:", z_gate.output)
            wires_to_change.add(z_gate.output)
    
    # Also check that all 2 inputs go into an xor and an and together
    # for x_0, y_0 in zip(x_gates, y_gates):
        


    # First, check that x00 and y00 make a half adder
    # if not all(xy in z_gate[0].inputs for xy in ["x00", "y00"]):
    #     wires_to_change.add("z00")
    # z00carry = gates_by_input["x00"]



submit_result_day(24, 1, solve_part_1())

