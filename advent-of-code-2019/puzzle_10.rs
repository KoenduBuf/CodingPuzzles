type Matrix = std::vec::Vec<std::vec::Vec<u32>>;
type Loc = (usize, usize);

fn get_input() -> Matrix {
    let str_in =
"#.#....#.#......#.....#......####.
#....#....##...#..#..##....#.##..#
#.#..#....#..#....##...###......##
...........##..##..##.####.#......
...##..##....##.#.....#.##....#..#
..##.....#..#.......#.#.........##
...###..##.###.#..................
.##...###.#.#.......#.#...##..#.#.
...#...##....#....##.#.....#...#.#
..##........#.#...#..#...##...##..
..#.##.......#..#......#.....##..#
....###..#..#...###...#.###...#.##
..#........#....#.....##.....#.#.#
...#....#.....#..#...###........#.
.##...#........#.#...#...##.......
.#....#.#.#.#.....#...........#...
.......###.##...#..#.#....#..##..#
#..#..###.#.......##....##.#..#...
..##...#.#.#........##..#..#.#..#.
.#.##..#.......#.#.#.........##.##
...#.#.....#.#....###.#.........#.
.#..#.##...#......#......#..##....
.##....#.#......##...#....#.##..#.
#..#..#..#...........#......##...#
#....##...#......#.###.#..#.#...#.
#......#.#.#.#....###..##.##...##.
......#.......#.#.#.#...#...##....
....##..#.....#.......#....#...#..
.#........#....#...#.#..#....#....
.#.##.##..##.#.#####..........##..
..####...##.#.....##.............#
....##......#.#..#....###....##...
......#..#.#####.#................
.#....#.#..#.###....##.......##.#.";
    let mut total = vec![];
    for line in str_in.lines() {
        let mut row = vec![];
        for char in line.chars() {
            if char == '.' {
                row.push(0);
            } else if char == '#' {
                row.push(1);
            }
        }
        total.push(row);
    }
    return total;
}

fn line_of_sight(p1: Loc, p2: Loc, tot_matrix: &Matrix) -> bool {
    let x_diff = p1.0 as i32 - p2.0 as i32;
    let y_diff = p1.1 as i32 - p2.1 as i32;
    if x_diff == 1 || y_diff == 1 || x_diff == -1 || y_diff == -1 {
        return true;
    }

    let dir = y_diff as f64 / x_diff as f64;

    // println!("\tDir: {}", dir);
    for r in 0..tot_matrix.len() {
        for e in 0..tot_matrix[r].len() {
            let test_x_diff = p1.0 as i32 - e as i32;
            let test_y_diff = p1.1 as i32 - r as i32;

            let test_dir = test_y_diff as f64 / test_x_diff as f64;
            if (dir.is_infinite() && test_dir.is_infinite()) || test_dir + 0.0000001 > dir && test_dir - 0.0000001 < dir {
                // println!("\tAstroid at {}, {} in dir, test_x_diff: {}, x_diff: {}", e, r, test_x_diff, x_diff);

                let same_x_dir = (test_x_diff > 0 && x_diff > 0) || (test_x_diff <= 0 && x_diff <= 0);
                let same_y_dir = (test_y_diff > 0 && y_diff > 0) || (test_y_diff <= 0 && y_diff <= 0);
                if tot_matrix[r][e] != 0 &&
                (test_x_diff.abs() < x_diff.abs() || test_y_diff.abs() < y_diff.abs()) && same_x_dir && same_y_dir {
                    // println!("\tAstroid at {}, {} in los", e, r);
                    // println!("\tDir: {},  Test dir: {}", dir, test_dir);
                    // some astroid in los
                    return false;
                }
            }
        }
    }
    return true;
}

fn increase_astroid(check: Loc, tot_matrix: &Matrix) -> u32 {
    let mut total_los = 0;
    for (r, _row) in tot_matrix.iter().enumerate() {
        for (e, _entry) in _row.iter().enumerate() {
            if *_entry != 0u32 && !(check.0 == e && check.1 == r) {
                // println!("Checking los with {},{}", e, r);
                if line_of_sight(check, (e, r), &tot_matrix) {
                    total_los += 1;
                    // println!("\tGOT IT");
                // } else {
                    // println!("\tNope");
                }
            }
        }
    }
    return total_los;
}

fn increase_by_views(tot_matrix: &mut Matrix) {
    for r in 0..tot_matrix.len() {
        for e in 0..tot_matrix[r].len() {
            if tot_matrix[r][e] == 0 { continue; }
            tot_matrix[r][e] = increase_astroid((e, r), &tot_matrix);
        }
    }
}

fn main() {
    let mut tot_matrix = get_input();

    // let res = increase_astroid((4, 2), &tot_matrix);
    // println!("Got res {}", res);

    increase_by_views(&mut tot_matrix);

    let mut best = 0;
    let mut best_loc: Loc = (0, 0);
    for (r, row) in tot_matrix.iter().enumerate() {
        for (e, ast) in row.iter().enumerate() {
            print!("{: ^5}", ast);
            if best < *ast {
                best = *ast;
                best_loc = (e, r);
            }
        }
        println!();
    }

    println!("\nBest: {}", best);
    println!("Loc: {}, {}", best_loc.0, best_loc.1);
}
