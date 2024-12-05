public class _4___LargestPalindromeProduct {
    public static void main(String[] args) {
        long largest = 0;
        for(int i = 999; i > 0; i--) {
            for(int j = 999; j > 0; j--) {
                //double tests, who cares
                if (isPalin(i * j)){
                    if (i * j > largest) {
                        largest = i * j;
                    }
                }
            }
        }
        System.out.println(largest);
    }
    public static boolean isPalin(long l) {
        char[] chars = String.valueOf(l).toCharArray();
        for (int i = 0; i < chars.length/2; i++) {
            if (chars[i] != chars[chars.length-1-i]) {
                return false;
            }
        }
        return true;
    }
}
