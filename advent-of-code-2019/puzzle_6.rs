use std::fs::File;
use std::io::{prelude::*, BufReader};
use std::collections::VecDeque;


fn get_input() -> Vec<(String, String)> {
    let file = File::open("puzzle_6.in").unwrap();
    let reader = BufReader::new(file);
    let mut vec = Vec::new();
    for line in reader.lines() {
        let uw = line.unwrap();
        let sp = uw.split(")").collect::<Vec<&str>>();
        let tpl = (sp[0].to_string(), sp[1].to_string());
        vec.push(tpl);
    }
    return vec;
}

fn bfs(input: &Vec<(String, String)>, start: String, find_end: Option<String>) {
    let mut queue = VecDeque::new();
    queue.push_back( (&start, 0, None) );

    let mut toend = 0;
    let mut total = 0;

    while !queue.is_empty() {
        // .0 = The node we are at; .1 = The steps from start; .2 = Parent
        let next = queue.pop_front().unwrap();


        if (&find_end).is_some() && next.0 ==
            (&find_end).as_ref().unwrap() {
            // If we found the end
            toend = next.1;
        }


        for combo in input {
            if &combo.0 == next.0 && ( (&next).2.is_none() || (&next).2.unwrap() != &combo.1 ) {
                // If this 'combo.1' orbits 'next':
                queue.push_back( (&combo.1, next.1 + 1, Some(&combo.0)) );
                total += next.1 + 1;
            }
            if &combo.1 == next.0 && ( (&next).2.is_none() || (&next).2.unwrap() != &combo.0 ) {
                // If 'next' orbits 'combo.0':
                queue.push_back( (&combo.0, next.1 + 1, Some(&combo.1)) );
                total += next.1 + 1;
            }
        }
    }

    println!("\nBFS from {} to {}", start, find_end.as_ref().unwrap_or(&"-".to_string()));
    println!("Found total (sub) orbits: {}", total);
    if find_end.is_none() {
        println!("Did not find an end.");
    } else {
        println!("Found total steps to end: {}", toend);
        println!("Found total answer moves: {}\n", toend - 2);
    }
}



fn main() {
    let input = get_input();

    let _com = "COM".to_string();
    let _you = "YOU".to_string();
    let _san = "SAN".to_string();

    bfs(&input, _com, None);
    bfs(&input, _you, Some(_san));
}
