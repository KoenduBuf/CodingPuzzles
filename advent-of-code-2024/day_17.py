from aoc_general import *


class OperandType:
    def get_value(self, machine, operand):
        raise NotImplementedError()

class ValueOperand(OperandType):
    def get_value(self, machine, operand):
        return operand

class ComboOperand(OperandType):
    def get_value(self, machine, operand):
        if operand <= 3:
            return operand
        return machine.get_reg(chr(ord('A') + operand - 4))

class Instruction:
    def __init__(self, name, opcode, operand_types, function):
        self.name = name
        self.opcode = opcode
        self.operand_types = operand_types
        self.function = function
    
    def uses_registers(self, operands):
        tryout_machine = MachineState()
        self.execute(tryout_machine, operands)
        return [ r for r in "ABC" if tryout_machine.stat_register_gets[tryout_machine._get_reg_index(r)] > 0 ]
    
    def writes_registers(self, operands):
        tryout_machine = MachineState()
        self.execute(tryout_machine, operands)
        return [ r for r in "ABC" if tryout_machine.stat_register_sets[tryout_machine._get_reg_index(r)] > 0 ]

    def execute(self, machine, operands):
        operand_values = [ t.get_value(machine, v) for t, v in zip(self.operand_types, operands) ]
        self.function(machine, *operand_values)

class MachineState:
    def __init__(self):
        self.registers = [ 0, 0, 0 ]
        self.instruction_pointer = 0
        self.output_buffer = []
        self.stat_register_gets = [0, 0, 0]
        self.stat_register_sets = [0, 0, 0]

    def _get_reg_index(self, reg):
        if isinstance(reg, str):
            return ord(reg) - ord('A')
        return reg

    def get_reg(self, reg):
        reg_idx = self._get_reg_index(reg)
        self.stat_register_gets[reg_idx] += 1
        return self.registers[reg_idx]

    def set_reg(self, reg, value):
        reg_idx = self._get_reg_index(reg)
        self.stat_register_sets[reg_idx] += 1
        self.registers[reg_idx] = value
    
    def jump_to_instruction(self, instruction):
        self.instruction_pointer = instruction

    def output(self, value):
        self.output_buffer.append(value)

    def get_output_str(self):
        return ",".join([ str(i) for i in self.output_buffer ])
    
    def run_single_instruction(self, code):
        opcode = code[self.instruction_pointer]
        instruction = instruction_map[opcode]
        operands = code[self.instruction_pointer + 1:self.instruction_pointer + 1 + len(instruction.operand_types)]
        instruction.execute(self, operands)
        self.instruction_pointer += 1 + len(instruction.operand_types)

    def state_tuple(self):
        return (tuple(self.registers), self.instruction_pointer)

    def run_program(self, code, until_outputs=-1):
        been_in_states = set()
        while self.instruction_pointer < len(code):
            if self.state_tuple() in been_in_states:
                return
            been_in_states.add(self.state_tuple())
            self.run_single_instruction(code)
            if len(self.output_buffer) == until_outputs:
                return
    
    def copy(self):
        new_machine = MachineState()
        new_machine.registers = self.registers.copy()
        new_machine.instruction_pointer = self.instruction_pointer
        new_machine.output_buffer = self.output_buffer.copy()
        return new_machine

# Instructions

instruction_set = [
    Instruction('adv', 0, [ ComboOperand() ], lambda machine, operand: machine.set_reg('A', machine.get_reg('A') // (2 ** operand))),
    Instruction('bxl', 1, [ ValueOperand() ], lambda machine, operand: machine.set_reg('B', machine.get_reg('B') ^ operand)),
    Instruction('bst', 2, [ ComboOperand() ], lambda machine, operand: machine.set_reg('B', operand % 8)),
    Instruction('jnz', 3, [ ValueOperand() ], lambda machine, operand: machine.get_reg('A') != 0 and machine.jump_to_instruction(operand - 2)),
    Instruction('bxc', 4, [ ValueOperand() ], lambda machine, _: machine.set_reg('B', machine.get_reg('B') ^ machine.get_reg('C'))),
    Instruction('out', 5, [ ComboOperand() ], lambda machine, operand: machine.output(operand % 8)),
    Instruction('bdv', 6, [ ComboOperand() ], lambda machine, operand: machine.set_reg('B', machine.get_reg('A') // (2 ** operand))),
    Instruction('cdv', 7, [ ComboOperand() ], lambda machine, operand: machine.set_reg('C', machine.get_reg('A') // (2 ** operand))),
]

instruction_map = { instruction.opcode: instruction for instruction in instruction_set }

# Parse input

def read_setup():
    init_str, instr_str = read_input_day(17).split("\n\n")
    init_str_lines = init_str.split("\n")
    machine = MachineState()
    machine.set_reg('A', int(init_str_lines[0].split(" A: ")[1]))
    machine.set_reg('B', int(init_str_lines[1].split(" B: ")[1]))
    machine.set_reg('C', int(init_str_lines[2].split(" C: ")[1]))
    code = [ int(i) for i in instr_str.split(" ")[1].split(",") ]
    return machine, code

# Solve

def solve_part_1():
    machine, code = read_setup()
    machine.run_program(code)
    return machine.get_output_str()

def solve_part_2_assumptions():
    machine, code = read_setup()
    looking_for_tuple = tuple(code)

    # Check there is only jumps to the start
    for i in range(0, len(code), 2):
        instr = instruction_map[code[i]]
        operand = code[i + 1]
        if instr.opcode == 3 and operand != 0:
            raise Exception("Not only jumps to start")
        
    # Create a map of when each register is first read/written
    first_reads, first_writes, total_writes = {}, {}, {}
    for i in range(0, len(code), 2):
        instr = instruction_map[code[i]]
        operand = code[i + 1]
        for reg in instr.uses_registers([operand]):
            if reg not in first_reads:
                first_reads[reg] = i
        for reg in instr.writes_registers([operand]):
            if reg not in first_writes:
                first_writes[reg] = i
            total_writes.setdefault(reg, 0)
            total_writes[reg] += 1

    # Check that B and C are derived from A
    if first_reads.get('B', 1000) < first_writes.get('B', 1000) or first_reads.get('C', 1000) < first_writes.get('C', 1000):
        raise Exception("B and/or C are not derived from A")
    
    # Check that A is only written to once, and it is a '>> 3'
    if total_writes.get('A', 0) != 1 or code[first_writes['A']] != 0 or code[first_writes['A'] + 1] != 3:
        raise Exception("A is not only written to once, or it is not a '>> 3'")

    # Find the first number that gives the first right output.
    # Then freeze the right 3 bits, and find the next number that gives the next right output.
    # To try is [ (frozen_number, frozen_bits, correct_output_values) ]
    FREEZE_BITS_PER_TIME = 3
    REQUIRED_BITS_PER_OUTPUT = 3
    MAX_BITS_EVER = REQUIRED_BITS_PER_OUTPUT * len(code)
    to_try = [ (0, 0, 0) ]
    in_try_queue = set()
    minimal_correct_answer = float('inf')
    while len(to_try) > 0:
        frozen_num, frozen_bits, prev_correct_output_values = to_try.pop()
        
        for next_bits in range(0, 1 << (REQUIRED_BITS_PER_OUTPUT * 4)):
            new_a = frozen_num | (next_bits << frozen_bits)
            if new_a > minimal_correct_answer:
                continue
            
            # Run the program with the new A value
            try_machine = machine.copy()
            try_machine.set_reg('A', new_a)
            try_machine.run_program(code)

            # Check if the output is exactly correct, store it if it is
            if looking_for_tuple == tuple(try_machine.output_buffer):
                print(f"Correct new minimal input value found: {new_a}")
                minimal_correct_answer = new_a
                continue

            # See if we are even allowed to continue
            if frozen_bits > MAX_BITS_EVER:
                continue

            # Check how many output values are correct & incorrect
            correct_output_values = 0
            for a, b in zip(try_machine.output_buffer, code):
                if a != b:
                    break
                correct_output_values += 1
            
            if correct_output_values > prev_correct_output_values:
                new_frozen_bits = frozen_bits + FREEZE_BITS_PER_TIME
                new_frozen_num = new_a & ((1 << new_frozen_bits) - 1)
                try_tuple = (new_frozen_num, new_frozen_bits, correct_output_values)
                if try_tuple in in_try_queue:
                    continue
                print(f"Found {tuple(try_machine.output_buffer[:correct_output_values])} / {tuple(try_machine.output_buffer[correct_output_values:])}, with value {new_a}, frozen: {new_frozen_bits} bits")
                to_try.append(try_tuple)
                in_try_queue.add(try_tuple)
    
    return minimal_correct_answer


def solve_part_2_brute_force():
    machine, code = read_setup()
    looking_for = ",".join([ str(i) for i in code ])

    for i in range(1 << 45, 1 << 48):
        # Run very short:
        try_machine = machine.copy()
        try_machine.set_reg('A', i)
        try_machine.run_program(code, 1)
        if try_machine.output_buffer[0] != code[0]:
            continue
        print("Found a possible start:", i)
        # If there is a chance, run the whole program
        try_machine = machine.copy()
        try_machine.set_reg('A', i)
        try_machine.run_program(code)
        if try_machine.get_output_str() == looking_for:
            return i
        
    raise Exception("Not found")

machine, code = read_setup()


def get_output_for_value(value):
    try_machine = machine.copy()
    try_machine.set_reg('A', value)
    try_machine.run_program(code)
    return try_machine

submit_result_day(17, 1, solve_part_1(), allow_non_numeric=True)

submit_result_day(17, 2, solve_part_2_assumptions())

# Program given: 2,4,  1,1,  7,5,  1,4,  0,3,  4,5,  5,5,  3,0
# B = A % 8                 # B = 0-7
# B = B ^ 1                 # B = 0-7
# C = A >> B                # Last 3 of C = 0-10 from the last of A.
# B = B ^ 4                 # Last 3 of B, determined by last 3 of B
# A = A >> 3
# B = B ^ C                 # Last 3 of B, determined by last 3 of B and C
# Output B % 8              # Output last 3 of B
# If A != 0, jump to 0

# Conclusion:
# Answer is '3 * len' bits
# And output is based on next 10 bits of A