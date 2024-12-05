public class DigitalSignature290 {
    public static void main(String[] args) {
        long res = 0;
        for (long n = 0; n < 10000000000000000L; n++) {
            if (sumDigits(n) == sumDigits(137*n)) {
                res++;
//                System.out.println(n);
            }
            if (n % 1000000 == 0) {
                System.out.println(n + " / " + 10000000000000000L + " - " + (double)n/(double)10000000000000000L);
            }
        }
        System.out.println(res);
    }

    private static int sumDigits(long input) {
        //first digit: input % 10
        int res = (int) (input % 10);
        //second digit: input % 100
        res += input % 100                  / 10;
        res += input % 1000                 / 100;
        res += input % 10000                / 1000;
        res += input % 100000               / 10000;
        res += input % 1000000              / 100000;
        res += input % 10000000             / 1000000;
        res += input % 100000000            / 10000000;
        res += input % 1000000000           / 100000000;
        res += input % 10000000000L         / 1000000000;
        res += input % 100000000000L        / 10000000000L;
        res += input % 1000000000000L       / 100000000000L;
        res += input % 10000000000000L      / 1000000000000L;
        res += input % 100000000000000L     / 10000000000000L;
        res += input % 1000000000000000L    / 100000000000000L;
        res += input % 10000000000000000L   / 1000000000000000L;
        res += input % 100000000000000000L  / 10000000000000000L;
        res += input % 1000000000000000000L / 100000000000000000L;
        res += input                        / 1000000000000000000L;
        return res;
    }
}
