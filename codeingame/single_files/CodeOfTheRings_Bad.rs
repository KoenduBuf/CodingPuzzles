use std::io;
use std::cell::RefCell;

macro_rules! parse_input {
    ($x:expr, $t:ident) => ($x.trim().parse::<$t>().unwrap())
}

/////////////////////////////////////////////////////////////////////
/////////////// Just some help with calculating charater indices etc.

// A B C D E .... X Y Z ' '
fn char_to_index(c: char) -> i32 {
    if ((c < 'A' || c > 'Z') && c != ' ') {
        panic!("Char not in range {}", c)
    }
    return if (c == ' ') { 26 } else { c as i32 - 'A' as i32 }
}
fn index_to_char(i: i32) -> char {
    if (i < -26 || i > 26) {
        panic!("Index not in range {}", i)
    }
    let ci: u8 = if (i >= 0) { i as u8 } else { 27 + i as u8 };
    if (ci == 26) { return ' '; }
    return ('A' as u8 + ci) as char
}
fn way_to(l1: i32, l2: i32, loop_at: i32) -> i32 {
    let dist = l2 - l1;
    let half = (loop_at/2) as i32;
    if (dist > half) { return (dist - loop_at) }
    if (dist < -half) { return (dist + loop_at) }
    return dist
}
fn char_dist(c1: char, c2: char) -> i32 {
    let index1 = char_to_index(c1);
    let index2 = char_to_index(c2);
    let dist = index2 - index1;
    return way_to(index1, index2, 27);
}

/////////////////////////////////////////////////////////////////////
////////////////////////// Things for calculating patterns in strings

fn string_sub_dup(s: &String) -> (usize, usize) { // returns (length, repeats)
    const at_least: usize = 4;
    if (s.len() < 2) { return (0, 0); }

    let mut pat_str = Vec::new();
    let chars = s.chars().collect::<Vec<char>>();
    let mut loopchars = s.chars();
    // pat_str.push(loopchars.next().unwrap());
    for nc in loopchars {
        pat_str.push(nc);

        if (pat_str.len() * at_least > s.len()) { break; }

        let mut repeats: usize = 0;
        'check: for check_at_index in (0..s.len() - pat_str.len()).step_by(pat_str.len()) {
            for i in 0..pat_str.len() {
                if (pat_str[i] != chars[i + check_at_index]) {
                    break 'check;
                }
            }
            repeats += 1;
        }
        if (repeats >= at_least) {
            return (pat_str.len(), repeats);
        }
    }
    return (0, 0);
}

/////////////////////////////////////////////////////////////////////
///////////////// The state struct, which keeps track of... the state

struct State {
    at_rune: usize,
    runes: [char;30],
    result: String
}

impl State {
    fn new() -> State {
        return State { at_rune: 0, 
            runes: [' '; 30],
            result: String::new() }
    }

    fn cmd_char(&mut self, c: char) {
        match c {
            '+' => self.runes[self.at_rune] = match self.runes[self.at_rune] {
                ' ' => 'A',
                'Z' => ' ',
                _ => (self.runes[self.at_rune] as u8 + 1) as char
            },
            '-' => self.runes[self.at_rune] = match self.runes[self.at_rune] {
                ' ' => 'Z',
                'A' => ' ',
                _ => (self.runes[self.at_rune] as u8 - 1) as char
            },
            '<' => self.at_rune = if (self.at_rune == 0) { 29 } else { self.at_rune - 1 },
            '>' => self.at_rune = (self.at_rune + 1) % 30,
            _ => { },
        };
        self.result.push(c);
    }

    fn cmd_char_n(&mut self, c: char, times: i32) {
        for i in 0..times { self.cmd_char(c) }
    }

    fn do_char_at(&mut self, to_loc: usize, c: char) {
        let loc_dist = way_to(self.at_rune as i32, to_loc as i32, 30);
        if (loc_dist < 0) {
            self.cmd_char_n('<', -loc_dist);
        } else if (loc_dist > 0) {
            self.cmd_char_n('>', loc_dist);
        }
        let dist = char_dist(self.runes[self.at_rune], c);
        if (dist < 0) {
            self.cmd_char_n('-', -dist);
        } else if (dist > 0) {
            self.cmd_char_n('+', dist);
        }
        self.cmd_char('.');
    }
}



// returns the location [0-29], the walk effort and the make effort
fn compute_effort(c:char, dloc: usize, state: &State) -> (usize, i32, i32) {
    let mut try_loc = state.at_rune + dloc;
    if (try_loc >= 30) { try_loc -= 30; }
    if (try_loc < 0) { try_loc += 30; }
    let try_char_dist = char_dist(state.runes[try_loc], c);
    return (try_loc, way_to(state.at_rune as i32, try_loc as i32,
        30).abs(), try_char_dist.abs());
}

fn make_letter(c: char, state: &mut State, start_of_pattern: bool, in_first_pattern: bool) {
    let mut have_start_char = false;
    for check in 0..30 { if (state.runes[state.at_rune] == c) { have_start_char = true } }

    let mut best_loc: i32 = -1;
    let mut best_dist = 100;
    for dloc in 0..30 {
        
        let (try_loc, walk_eff, make_eff) = compute_effort(c, dloc, &state);
        let mut try_effort = walk_eff + make_eff;

        if (in_first_pattern) {
            if (!start_of_pattern && dloc == 1) { try_effort -= 20; }
            if (start_of_pattern && dloc == 0) { try_effort -= 20; }
        }
        if (start_of_pattern && have_start_char && make_eff == 0) {
            try_effort -= 20;
        }

        if (try_effort > best_dist) { continue; }
        best_loc = try_loc as i32;
        best_dist = try_effort;
    }
    state.do_char_at(best_loc as usize, c);
}



fn goes_into_dir(st: &String) -> (i32, i32) {
    let mut at = 0;
    let mut min = 0;
    let mut max = 0;
    for c in st.chars() {
        match c {
            '<' => at -= 1,
            '>' => at += 1,
            _ => {}
        }
        if (at < min) { min = at; }
        if (at > max) { max = at; }
    }
    return (-min, max);
}

fn reduce_and_print(result: String) {
    let mut reduced = String::new();

    let mut next = 0;
    while (next < result.len()) {
        let mut chars = result.chars();
        let st: String = (&mut chars).skip(next).collect();
        let first_char = st.chars().next().unwrap();

        let (len, mut rep) = string_sub_dup(&st);
        eprintln!("char {} ?? {} long, {} times", first_char, len, rep);
        if (rep >= 26) { rep = 26; }
        if (len >= 1 && (rep * len > (27 - rep) + 7 + len)) {
            // normally: rep * len
            // this way: (27 - rep) + 7 + len
            let (left, right) = goes_into_dir(&st.chars().take(len).collect());
            eprintln!("Can reduce! {} long, {} times (left {})", len, rep, left);

            // let mut counter_at = 0;
            if (left != 0) {
                reduced.push(first_char);
                next += 1;
                continue;
            }
            // if (left > right) {
            //     counter_at = right + 1;
            // } else {
            //     counter_at = -left - 1;
            // }

            // if (counter_at < 0) { for i in 0..-counter_at { reduced.push('<'); } }
            // if (counter_at > 0) { for i in 0..counter_at { reduced.push('>'); } }


            reduced.push_str("<");
            for t in 0..27-rep {
                reduced.push('-');
            }
            reduced.push_str("[>");
            let looped_string: String = st.chars().take(len).collect();
            reduced.push_str(looped_string.as_str());
            reduced.push_str("<-]>");
            next += (len * rep);
            continue;
        }


        reduced.push(first_char);
        next += 1;
    }

    println!("{}", reduced);
}








fn main() {
    let mut input_line = String::new();
    io::stdin().read_line(&mut input_line).unwrap();
    let magic_phrase = input_line.trim_matches('\n').to_string();

    let mut state = State::new();

    let mut first_pattern = false;
    let mut lastLen: i32 = -1;
    let mut lastRep = 0;

    for i in 0..magic_phrase.len() {
        let mut chars = magic_phrase.chars();
        let st: String = (&mut chars).skip(i).collect();
        let first_char = st.chars().next().unwrap();
        
        // eprintln!("Got char {}, rest is {}", first_char, st);
        let (len, rep) = string_sub_dup(&st);
        let mut pattern_start = false;
        if (lastLen == -1 || lastLen == len as i32) { // Talking about same pattern
            if (lastRep != rep) {
                first_pattern = lastLen == -1;
                pattern_start = true;
            }
        }
        lastLen = len as i32;
        lastRep = rep;

        // eprintln!("Repitition? {} long, {} times ({} start {} first)", len, rep, pattern_start, first_pattern);
        make_letter(first_char, &mut state, pattern_start, first_pattern);
    }

    reduce_and_print(state.result)


    
}

