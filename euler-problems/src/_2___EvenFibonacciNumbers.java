public class _2___EvenFibonacciNumbers {
    public static void main(String[] args) {
        long res = 2;

        int twoBefore = 1;
        int oneBefore = 2;
        while (true) {
            int newV = twoBefore + oneBefore;
            if (newV > 4000000) break;
            twoBefore = oneBefore;
            oneBefore = newV;

            if (newV % 2 == 0) {
                res += newV;
            }


            if (res > Long.MAX_VALUE - 4000000) {
                System.out.println("OVERFLOW ALERT");
            }
        }
        System.out.println(res);
    }
}
