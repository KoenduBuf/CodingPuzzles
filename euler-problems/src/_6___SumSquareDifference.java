public class _6___SumSquareDifference {
    public static void main(String[] args) {
        long sumOfSquares = 0;
        long sum = 0;
        for (int i = 1; i <= 100; i++) {
            sum += i;
            sumOfSquares += (i * i);
        }
        System.out.println((sum * sum) - sumOfSquares);
    }
}
