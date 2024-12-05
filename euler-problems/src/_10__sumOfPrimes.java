public class _10__sumOfPrimes {
    public static void main(String[] args) {
        long res = 0;
        for (int i = 0; i < 2000000; i++) {
            if (_3___LargestPrimeFactor.isPrime(i)) {
                res += i;
            }
        }
        System.out.println(res);
    }
}
