public class _7___10001stPrime {
    public static void main(String[] args) {
        long xst = 10001;
        for (long x = 2; x < Long.MAX_VALUE; x++) {
            if (_3___LargestPrimeFactor.isPrime(x)) {
                xst--;
            }
            if (xst == 0) {
                System.out.println(x);
                return;
            }
        }
    }


}
