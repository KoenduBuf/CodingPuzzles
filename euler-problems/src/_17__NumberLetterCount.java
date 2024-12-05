public class _17__NumberLetterCount {
    public static void main(String[] args) {
        long total = 0;
        for (int i = 1; i <= 1000; i++) {
            String w = toWord(i);
//            System.out.println(w);
            total += w.length();
        }
        System.out.println(total);
    }

    public static String toWord(int i) {
        if (i <= 0) return null;

        if (i < 10) {
            switch (i) {
                case 1: return "one";
                case 2: return "two";
                case 3: return "three";
                case 4: return "four";
                case 5: return "five";
                case 6: return "six";
                case 7: return "seven";
                case 8: return "eight";
                case 9: return "nine";
            }
        }

        if (i < 20) {
            switch (i) {
                case 10: return "ten";
                case 11: return "eleven";
                case 12: return "twelve";
                case 13: return "thirteen";
                case 14: return "fourteen";
                case 15: return "fifteen";
                default: return toWord(i % 10) + "teen";
            }
        }

        switch (i) {
            case 20: return "twenty";
            case 30: return "thirty";
            case 40: return "forty";
            case 50: return "fifty";
            case 60: return "sixty";
            case 70: return "seventy";
            case 80: return "eighty";
            case 90: return "ninety";
        }

        if (i < 100) {
            return toWord((i / 10) * 10) + toWord(i % 10);
        }

        if (i < 1000) {
            String hund = toWord(i/100) + "hundred";
            if (i % 100 == 0) {
                return hund;
            }
            return hund + "and" + toWord(i%100);
        }
        if (i == 1000) return "onethousand";
        return null;
    }
}
