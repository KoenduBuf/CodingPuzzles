public class _3___LargestPrimeFactor {
    public static void main(String[] args) {
        long toTest = 600851475143L;

        for (int i = 2; i < toTest; i++) {
            if (toTest % i == 0) {
                long p = toTest/i;
                if (isPrime(p)) {
                    System.out.println(p);
                    return;
                }
            }

        }
    }

    public static boolean isPrime(long l) {
        if (l <= 1) return false;
        if (l <= 3) return true;
        if (l % 2 == 0 || l % 3 == 0) return false;

        for (int i = 5; i*i <= l; i+=6) {
            if (l % i == 0 || l % (i+2) == 0) {
                return false;
            }
        }
        return true;
    }
}
