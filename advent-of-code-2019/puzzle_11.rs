mod int_code_64;
use std::collections::HashSet;

struct Vec2 {
    x: i32,
    y: i32
}

static UP: Vec2      = Vec2 { x:  0, y:  1 };
static RIGHT: Vec2   = Vec2 { x:  1, y:  0 };
static DOWN: Vec2    = Vec2 { x:  0, y: -1 };
static LEFT: Vec2    = Vec2 { x: -1, y:  0 };
static DIRECTIONS: [&Vec2; 4] = [&UP, &RIGHT, &DOWN, &LEFT];



fn make_code() -> std::vec::Vec<i64> {
     return vec![3,8,1005,8,311,1106,0,11,0,0,0,104,1,104,0,3,8,1002,8,-1,10,101,1,10,10,4,10,108,0,8,10,4,10,1002,8,1,28,2,103,7,10,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,1,10,4,10,1001,8,0,55,2,3,6,10,1,101,5,10,1,6,7,10,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,0,10,4,10,1001,8,0,89,1,1108,11,10,2,1002,13,10,1006,0,92,1,2,13,10,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,0,10,4,10,101,0,8,126,3,8,1002,8,-1,10,101,1,10,10,4,10,108,1,8,10,4,10,1002,8,1,147,1,7,0,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,0,8,10,4,10,101,0,8,173,1006,0,96,3,8,102,-1,8,10,101,1,10,10,4,10,108,0,8,10,4,10,1001,8,0,198,1,3,7,10,1006,0,94,2,1003,20,10,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,1,10,4,10,102,1,8,232,3,8,102,-1,8,10,101,1,10,10,4,10,108,1,8,10,4,10,102,1,8,253,1006,0,63,1,109,16,10,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,1,10,4,10,101,0,8,283,2,1107,14,10,1,105,11,10,101,1,9,9,1007,9,1098,10,1005,10,15,99,109,633,104,0,104,1,21102,837951005592,1,1,21101,328,0,0,1105,1,432,21101,0,847069840276,1,21101,0,339,0,1106,0,432,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21102,179318123543,1,1,21102,386,1,0,1106,0,432,21102,1,29220688067,1,21102,1,397,0,1106,0,432,3,10,104,0,104,0,3,10,104,0,104,0,21102,709580567396,1,1,21102,1,420,0,1105,1,432,21102,1,868498694912,1,21102,431,1,0,1106,0,432,99,109,2,22101,0,-1,1,21101,40,0,2,21101,0,463,3,21101,0,453,0,1105,1,496,109,-2,2106,0,0,0,1,0,0,1,109,2,3,10,204,-1,1001,458,459,474,4,0,1001,458,1,458,108,4,458,10,1006,10,490,1102,1,0,458,109,-2,2105,1,0,0,109,4,1202,-1,1,495,1207,-3,0,10,1006,10,513,21102,0,1,-3,21201,-3,0,1,21202,-2,1,2,21101,0,1,3,21101,0,532,0,1106,0,537,109,-4,2106,0,0,109,5,1207,-3,1,10,1006,10,560,2207,-4,-2,10,1006,10,560,22102,1,-4,-4,1105,1,628,21201,-4,0,1,21201,-3,-1,2,21202,-2,2,3,21101,0,579,0,1105,1,537,22101,0,1,-4,21102,1,1,-1,2207,-4,-2,10,1006,10,598,21102,1,0,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,620,22102,1,-1,1,21101,0,620,0,106,0,495,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2106,0,0];
}

const SIZE: usize = 100;


struct Robot {
    dir: usize,
    pub location: Vec2,
    brain: int_code_64::IntCodeMachine,
    move_num: u32
}

impl Robot {
    fn turn(&mut self, left: bool) {
        if left {
            if self.dir == 0 {
                self.dir = 3;
            } else {
                self.dir -= 1;
            }
        } else {
            if self.dir == 3 {
                self.dir = 0;
            } else {
                self.dir += 1;
            }
        }
    }

    fn run(&mut self, black: bool, field: &mut [ [bool; SIZE]; SIZE ]) -> bool {
        if self.move_num == 0 || self.brain.running {
            self.brain.input(if black { 0 } else { 1 });
            self.brain.run();
        } else {
            return true;
        }

        if self.brain.output((self.move_num * 2) as usize) == 0 {
            // Paint black
            field[self.field_x()][self.field_y()] = true;
        } else {
            // Paint white
            field[self.field_x()][self.field_y()] = false;
        }

        self.turn(self.brain.output((self.move_num * 2 + 1) as usize) == 0);
        self.location.x += DIRECTIONS[self.dir].x;
        self.location.y += DIRECTIONS[self.dir].y;
        self.move_num += 1;
        return false;
    }

    fn field_x(&self) -> usize {
        return (self.location.x + SIZE as i32 / 2) as usize;
    }
    fn field_y(&self) -> usize {
        return (self.location.y + SIZE as i32 / 2) as usize;
    }
}




fn main() {
    let brain = int_code_64::IntCodeMachine::new(make_code(), vec![], vec![], true, true);
    let mut bot = Robot{ dir: 0, brain: brain, location: Vec2 { x: 0, y: 0 }, move_num: 0 };

    let mut changed = HashSet::new();

    let mut field = [ [true; SIZE ]; SIZE ];
    field[bot.field_x()][bot.field_y()] = false;
    let mut color = false;

    while !bot.run(color, &mut field) {
        changed.insert( (bot.field_x(), bot.field_y()) );
        color = field[bot.field_x()][bot.field_y()];
    }
    println!();

    for x in 0..SIZE {
        for y in 0..SIZE {
            print!("{}", if field[x][y] { '.' } else { '#' });
        }
        println!();
    }

    println!("Changed {}", changed.len());
}
// UZAEKBLP
