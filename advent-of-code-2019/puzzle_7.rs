mod intcode1;

fn make_code() -> std::vec::Vec<i32> {
    // return vec![3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]; // Chaining (5) with inputs 43210 should  give 43210

    // return vec![3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5];

    return vec![3,8,1001,8,10,8,105,1,0,0,21,34,47,72,81,94,175,256,337,418,99999,3,9,102,3,9,9,1001,9,3,9,4,9,99,3,9,101,4,9,9,1002,9,5,9,4,9,99,3,9,1001,9,5,9,1002,9,5,9,1001,9,2,9,1002,9,5,9,101,5,9,9,4,9,99,3,9,102,2,9,9,4,9,99,3,9,1001,9,4,9,102,4,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,99];
}

fn run_chain(length: usize, all_inputs: std::vec::Vec<i32>) -> i32 {
    let mut machines = vec![];

    for i in 0..length {
        let code = make_code();

        let output = vec![];
        let mut inputs = vec![ all_inputs[i] ];
        if i == 0 {
            inputs.push(0);
        }

        let machine = intcode1::IntCodeMachine::new(code, inputs, output, true, true);
        machines.push(machine);
    }

    let mut loopy = 0;
    let mut output = 0i32;
    println!("Machines {}", machines.len());
    loop {
        if loopy != 0 && !machines[0].running {
            return output;
        }
        // For every machine
        for i in 0..length {
            print!("Running machine {}", i);
            machines[i].run();
            print!("  Done  ");
            output = machines[i].output(loopy);
            println!("Output: {}", output);

            if loopy == 0 || machines[length - 1].running {
                machines[(i + 1) % length].input(output);
            }
        }

        loopy += 1;
    }

}


fn main() {
    let from = 5;
    let to = 10;
    let mut best = 0;

    for inA in from..to {
        for inB in from..to {
            if inB == inA { continue; }

            for inC in from..to {
                if inC == inA || inC == inB { continue; }

                for inD in from..to {
                    if inD == inA || inD == inB || inD == inC { continue; }

                    for inE in from..to {
                        if inE == inA || inE == inB || inE == inC || inE == inD { continue;  }

                        let res = run_chain(5, vec![inA, inB, inC, inD, inE]);
                        if  res > best {
                            best = res;
                        }
                    }
                }
            }
        }
    }

    println!("Best: {}", best);

}
