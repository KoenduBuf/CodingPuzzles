public class _1___MultiplesOf3And5 {
    public static void main(String[] args) {
        long res = 0;
        for (int i = 0; i < 1000; i++) {
            if (i % 3 == 0 || i % 5 == 0) {
                res += i;
            }
        }
        System.out.println(res);
    }
}
