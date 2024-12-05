public class _12__HighlyDivisibleTriangular {

    public static void main(String[] args) {
        long nextTri = 0;
        for (int i = 1; i < Integer.MAX_VALUE; i++) {
            nextTri += i;

            if (countTerms(nextTri) > 500) {
                System.out.println(nextTri);
                return;
            }
        }
    }

    public static int countTerms(long in) {
        int res = 0;
        for (int i = 1; i <= in/2; i++) {
            if (in % i == 0) {
                res++;
            }
        }
        return ++res;
    }
}
