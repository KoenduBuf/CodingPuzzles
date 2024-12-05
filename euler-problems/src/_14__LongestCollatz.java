public class _14__LongestCollatz {
    public static void main(String[] args) {
        long longestChain = -1;
        long startingNumber = -1;
        for (int i = 1; i < 1000000; i++) {
            long chainSize = numbersInChain(i);
            if (chainSize > longestChain) {
                longestChain = chainSize;
                startingNumber = i;
                System.out.println(i);
            }
        }
        System.out.println(startingNumber);
    }

    public static long numbersInChain(long at) {
        long loops = 1;
        while(at != 1) {
            if (at % 2 == 0) at = at/2;
            else at = (3*at) + 1;
            loops++;
        }
        return loops;
    }
}
