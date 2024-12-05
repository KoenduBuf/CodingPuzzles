public class _5___SmallestMultiple {
    public static void main(String[] args) {
        for (long a = 1; a < Long.MAX_VALUE; a++) {
            if (isEvenlyDivisible(a)) {
                System.out.println(a);
                return;
            }
        }
    }

    private static boolean isEvenlyDivisible(long l) {
        for (int i = 2; i <= 20; i++) {
            if (l % i != 0) {
                return false;
            }
        }
        return true;
    }
}
