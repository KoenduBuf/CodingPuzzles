use std::vec::Vec;


#[derive(Debug)]
struct Line {
    p1: Point,
    p2: Point
}

impl Line {
    fn vertical(&self) -> bool {
        return self.p1.x == self.p2.x;
    }

    fn max_x(&self) -> &Point {
        if self.p1.x >= self.p2.x {
            return &self.p1;
        }
        return &self.p2;
    }
    fn min_x(&self) -> &Point {
        if self.p1.x < self.p2.x {
            return &self.p1;
        }
        return &self.p2;
    }

    fn max_y(&self) -> &Point {
        if self.p1.y >= self.p2.y {
            return &self.p1;
        }
        return &self.p2;
    }
    fn min_y(&self) -> &Point {
        if self.p1.y < self.p2.y {
            return &self.p1;
        }
        return &self.p2;
    }

    fn len(&self) -> i32 {
        if self.vertical() {
            return (self.p1.y - self.p2.y).abs();
        } else {
            return (self.p1.x - self.p2.x).abs();
        }
    }

    fn intersects(&self, other: &Line) -> Option<Point> {
        if self.vertical() {
            if other.vertical() {
                if self.p1.x == other.p1.x {
                    println!("Multi point line intersecti, both vertical (returning None for ease)");
                }
                return None;
            } else {
                if other.min_x().x <= self.p1.x && other.max_x().x >= self.p1.x
                    && self.min_y().y <= other.p1.y && self.max_y().y >= other.p1.y {
                    return Some(Point { x: self.p1.x, y: other.p1.y });
                } else {
                    return None;
                }
            }
        }
        if other.vertical() {
            return other.intersects(self);
        } else {
            if self.p1.y == other.p1.y {
                println!("Line 1: {:?} -- {:?}", self.p1, self.p2);
                println!("Line 2: {:?} -- {:?}", other.p1, other.p2);
                println!("Multi point line intersect, both horizontal (returning None for ease)");
            }
            return None;
        }
    }
}

#[derive(Debug)]
struct Point {
    x: i32,
    y: i32
}



fn parse_line(line: &str) -> Vec<Line> {
    let mut loc1 = Point { x: 0, y: 0 };
    let mut loc2 = Point { x: 0, y: 0 };

    let part_it = line.split(",");
    let mut vec = Vec::new();

    for dir in part_it {
        let dir_char = dir.chars().next().unwrap();
        let val_char = dir[1..].parse::<i32>().unwrap();
        match dir_char {
            'U' => loc2.y += val_char,
            'R' => loc2.x += val_char,
            'D' => loc2.y -= val_char,
            'L' => loc2.x -= val_char,
            _ => println!("Unexpected dir char {}", dir_char)
        }
        let p1 = Point { x: loc1.x, y: loc1.y };
        let p2 = Point { x: loc2.x, y: loc2.y };
        // println!("Line from   {:?}   to   {:?}", p1, p2);
        vec.push(Line { p1: p1, p2: p2 });
        loc1.x = loc2.x;
        loc1.y = loc2.y;
    }
    vec.push(Line { p1: loc1, p2: loc2 });
    return vec;
}


fn map_to_steps(path: &Vec<Line>, p: &Point) -> u32 {
    let mut total_steps = 0u32;
    let mut at_pos = Point { x: 0, y: 0 };
    for line in path {
        if line.vertical() {
            let len = line.len();
            for _i in 0..len {
                if line.min_y().y == line.p1.y {
                    at_pos.y += 1;
                } else {
                    at_pos.y -= 1;
                }
                total_steps += 1;
                if at_pos.x == p.x && at_pos.y == p.y {
                    return total_steps;
                }
            }
        } else {
            let len = line.len();
            for _i in 0..len {
                if line.min_x().x == line.p1.x {
                    at_pos.x += 1;
                } else {
                    at_pos.x -= 1;
                }
                total_steps += 1;
                if at_pos.x == p.x && at_pos.y == p.y {
                    return total_steps;
                }

            }
        }
    }
    println!("Steps count not working...");
    return 0;
}


fn main() {
    let line1 = "R1009,U993,L383,D725,R163,D312,R339,U650,R558,U384,R329,D61,L172,D555,R160,D972,L550,D801,L965,U818,L123,D530,R176,D353,L25,U694,L339,U600,L681,D37,R149,D742,R762,U869,R826,U300,L949,U978,L303,U361,R136,D343,L909,U551,R745,U913,L566,D292,R820,U886,R205,D431,L93,D71,R577,U872,L705,U510,L698,U963,R607,U527,L669,D543,R690,U954,L929,D218,R490,U500,L589,D332,R949,D538,R696,U659,L188,U468,L939,U833,L445,D430,R78,D303,R130,D649,R849,D712,L511,U745,R51,U973,R799,U829,R605,D771,L837,U204,L414,D427,R538,U116,R540,D168,R493,U900,L679,U431,L521,D500,L428,U332,L954,U717,L853,D339,L88,U807,L607,D496,L163,U468,L25,U267,L759,D898,L591,U445,L469,U531,R596,D486,L728,D677,R350,D429,R39,U568,R92,D875,L835,D841,R877,U178,L221,U88,R592,U692,R455,U693,L419,U90,R609,U672,L293,U168,R175,D456,R319,D570,R504,D165,L232,D624,L604,D68,R807,D59,R320,D281,L371,U956,L788,D897,L231,D829,R287,D798,L443,U194,R513,D925,L232,U225,L919,U563,R448,D889,R661,U852,L950,D558,L269,U186,L625,U673,L995,U732,R435,U849,L413,D690,L158,D234,R361,D458,L271,U90,L781,U754,R256,U162,L842,U927,L144,D62,R928,D238,R473,U97,L745,U303,L487,D349,L520,D31,L825,U385,L133,D948,L39,U62,R801,D664,L333,U134,R692,U385,L658,U202,L279,D374,R489,D686,L182,U222,R733,U177,R94,D603,L376,U901,R216,D851,L155,D214,L460,U758,R121,D746,L180,U175,L943,U146,L166,D251,L238,U168,L642,D341,R281,U182,R539,D416,R553,D67,L748,U272,R257,D869,L340,U180,R791,U138,L755,D976,R731,U713,R602,D284,L258,U176,R509,U46,R935,U576,R96,U89,L913,U703,R833";
    let line2 = "L1006,D998,R94,D841,R911,D381,R532,U836,L299,U237,R781,D597,L399,D800,L775,D405,L485,U636,R589,D942,L878,D779,L751,U711,L973,U410,L151,U15,L685,U417,L106,D648,L105,D461,R448,D743,L589,D430,R883,U37,R155,U350,L421,U23,R337,U816,R384,D671,R615,D410,L910,U914,L579,U385,R916,U13,R268,D519,R289,U410,L389,D885,L894,U734,L474,U707,L72,U155,L237,U760,L127,U806,L15,U381,L557,D727,L569,U320,L985,D452,L8,D884,R356,U732,L672,D458,L485,U402,L238,D30,R644,U125,R753,U183,L773,U487,R849,U210,L164,D808,L595,D668,L340,U785,R313,D72,L76,D263,R689,U604,R471,U688,R462,D915,R106,D335,R869,U499,R190,D916,R468,D882,R56,D858,L143,D741,L386,U856,R50,U853,R151,D114,L773,U854,L290,D344,L23,U796,L531,D932,R314,U960,R643,D303,L661,D493,L82,D491,L722,U848,L686,U4,L985,D509,L135,D452,R500,U105,L326,D101,R222,D944,L645,D362,L628,U305,L965,U356,L358,D137,R787,U728,R967,U404,R18,D928,L695,D965,R281,D597,L791,U731,R746,U163,L780,U41,L255,U81,L530,D964,R921,D297,R475,U663,L226,U623,L984,U943,L143,U201,R926,U572,R343,U839,R764,U751,R128,U939,R987,D108,R474,U599,R412,D248,R125,U797,L91,D761,L840,U290,L281,U779,R650,D797,R185,D320,L25,U378,L696,U332,R75,D620,L213,D667,R558,U267,L846,U306,R939,D220,R311,U827,R345,U534,R56,D679,R48,D845,R898,U8,R862,D960,R753,U319,L886,D795,R805,D265,R876,U729,R894,D368,R858,U744,R506,D327,L903,U919,L721,U507,L463,U753,R775,D719,R315,U128,R17,D376,R999,D386,L259,U181,L162,U605,L265,D430,R35,D968,R207,U466,R796,D667,R93,U749,L315,D410,R312,U929,L923,U260,R638";



    //let line1 = "R8,U5,L5,D3"; //"R75,D30,R83,U83,L12,D49,R71,U7,L72";
    let l1vec = parse_line(&line1);

    //let line2 = "U7,R6,D4,L4"; //"U62,R66,U55,R34,D71,R55,D58,R83";
    let l2vec = parse_line(&line2);

    let mut inter = Vec::new();
    for l1 in &l1vec {
        for l2 in &l2vec {
            let p = l1.intersects(&l2);
            if p.is_some() {
                let i = p.unwrap();
                //println!("Intersect at {:?}", i);
                inter.push(i);
            }
        }
    }


    let min = inter.iter()
        .filter(|p| p.x != 0 || p.y != 0)
        .map(|p| (map_to_steps(&l1vec, p) + map_to_steps(&l2vec, p), p))
        //.map(|p| (p.x.abs() + p.y.abs(), p))
        .min_by(|t1, t2| t1.0.cmp(&t2.0)).unwrap().1;
    println!("min: {:?} --- dist: {}", min, map_to_steps(&l1vec, min) + map_to_steps(&l2vec, min));

}
