#[allow(dead_code)]
pub struct IntCodeMachine {
    // Inputs bascially
    code:   std::vec::Vec<i64>,
    inputs: std::vec::Vec<i64>,
    output: std::vec::Vec<i64>,
    use_inputs_only: bool,
    return_on_wait: bool,

    // Internal state
    pub running: bool,
    relative_base: i64,
    input_idx: u32,
    pc: usize
}

#[allow(dead_code)]
impl IntCodeMachine {
    pub fn new(code: std::vec::Vec<i64>, inputs: std::vec::Vec<i64>,
    output: std::vec::Vec<i64>, inputs_only: bool, ret_on_wait: bool) -> IntCodeMachine {
        return IntCodeMachine {
            code: code,
            inputs: inputs,
            output: output,
            use_inputs_only: inputs_only,
            return_on_wait: ret_on_wait,

            running: false,
            relative_base: 0,
            input_idx: 0,
            pc: 0
        }
    }

    fn single_int_input(&mut self) -> Option<i64> {
        // Check input vector
        if self.inputs.len() > self.input_idx as usize {
            let ret = self.inputs[self.input_idx as usize];
            self.input_idx += 1;
            return Some(ret);
        }
        // If only that allowed, wait or return
        if self.use_inputs_only {
            if self.return_on_wait {
                return None;
            }
            while self.inputs.len() <= self.input_idx as usize {
                // Should wait to not kill cpu
            }
            return self.single_int_input();
        }
        // Else read from stdin
        use std::io::stdin;
        let mut s = String::new();
        stdin().read_line(&mut s).expect("X");
        if let Some('\n') = s.chars().next_back() { s.pop(); }
        if let Some('\r') = s.chars().next_back() { s.pop(); }
        let parsed = s.parse::<i64>();
        if parsed.is_err() {
            panic!("Parse error to i64 for {}", s);
        }
        return Some(parsed.unwrap());
    }



    fn store_val(&mut self, val: i64, loc_idx: i64) {
        let loc = self.get_loc(loc_idx);
        if loc >= self.code.len() {
            self.code.resize(loc + 1, 0);
        }
        self.code[loc] = val;
    }

    fn get_val(&self, loc: usize) -> i64 {
        if loc >= self.code.len() {
            return 0;
        }
        return self.code[loc];
    }





    fn param_value(&self, idx: i64) -> i64 {
        return (self.code[self.pc] / 10i64.pow((idx + 1) as u32)) % 10;
    }

    fn get_loc(&self, idx: i64) -> usize {
        if idx == 0 { panic!("Got index 0 for get_loc"); }
        match self.param_value(idx) {
            0 => {
                return self.get_val(self.pc + (idx as usize)) as usize;
            }
            2 => {
                return (self.get_val(self.pc + idx as usize) + self.relative_base) as usize;
            }
            x => { panic!("Undefined loc mode {}", x); }
        }
    }

    fn get_param(&self, idx: i64) -> i64 {
        if idx == 0 { panic!("Got index 0 for get_param"); }
        // idx 1 => 3rd digit from the right
        match self.param_value(idx) {
            0 | 2 => { // position mode and relative mode
                return self.get_val(self.get_loc(idx));
            }
            1 => { // immediate mode
                return self.get_val(self.pc + (idx as usize));
            }
            x => { panic!("Undefined param mode {}", x); }
        }
    }



    pub fn run(&mut self) -> i64 {
        self.running = true;
        loop {
            match self.code[self.pc] % 100 {
                1 => { // Addition
                    self.store_val(self.get_param(1) + self.get_param(2), 3);
                    self.pc += 4;
                }
                2 => { // Multiplication
                    self.store_val(self.get_param(1) * self.get_param(2), 3);
                    self.pc += 4;
                }
                3 => { // Get int input
                    let input = self.single_int_input();
                    if input.is_none() { return 0; }
                    self.store_val(input.unwrap(), 1);
                    self.pc += 2;
                }
                4 => { // Output single int
                    let print = self.get_param(1);
                    print!("{}", print);
                    self.output.push(print);
                    self.pc += 2;
                }
                5 => { // If != 0
                    self.pc = if self.get_param(1) != 0
                        { self.get_param(2) as usize }
                        else { self.pc + 3 };
                }
                6 => { // If == 0
                    self.pc = if self.get_param(1) == 0
                        { self.get_param(2) as usize }
                        else { self.pc + 3 };
                }
                7 => { // compare <
                    self.store_val( if self.get_param(1) <
                        self.get_param(2) { 1 } else { 0 } , 3);
                    self.pc += 4;
                }
                8 => { // compare ==
                    self.store_val( if self.get_param(1) ==
                        self.get_param(2) { 1 } else { 0 } , 3);
                    self.pc += 4;
                }
                9 => {
                    self.relative_base += self.get_param(1);
                    self.pc += 2;
                }
                99 => {
                    self.running = false;
                    return self.get_val(0);
                }
                x => { panic!("Unrecognized opcode {}", x); }
            }
        }
    }




    /////////////////////////////////////////////
    //////// Fucntions for users to change state
    /////////////////////////////////////////////

    pub fn output(&self, idx: usize) -> i64 {
        if idx >= self.output.len() {
            panic!("Requested output {} but output len was {}",
                idx, self.output.len());
        }
        return self.output[idx];
    }

    pub fn input(&mut self, val: i64) {
        self.inputs.push(val);
    }


    /////////////////////////////////////////////
    ///////// Easy run option for just some code
    /////////////////////////////////////////////
    pub fn run_code(code: std::vec::Vec<i64>) -> i64 {
        let mut machine = IntCodeMachine::new(code, vec![], vec![], false, false);
        return machine.run();
    }
}
