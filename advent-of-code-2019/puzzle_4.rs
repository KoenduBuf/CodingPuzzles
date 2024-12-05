

fn main() {
    // let i = 2255;
    let mut total = 0;


    for i in 153517..630395 {
        let s = i.to_string();

        // let regex_2ch = Regex::new(r"(?m)([ 0-9])((?!\1)[0-9])\2((?!\2))").unwrap();
        // let regex_inc = Regex::new(r"(?m) 0*1*2*3*4*5*6*7*8*9*").unwrap();

        let mut works = true;
        let mut d_groups = 0;
        let mut now_adc = 0;
        let mut last_c = '0' ;

        for c in s.chars() {
            if c == last_c {
                if now_adc == 1 {
                    d_groups -= 1;
                } else if now_adc == 0 {
                    d_groups += 1;
                }
                now_adc += 1;
            } else {
                now_adc = 0;
            }

            if c < last_c {
                works = false;
            }
            last_c = c;
        }

        if works && d_groups >= 1 {
            total += 1;
        }
    }

    println!("total: {}", total);
}
