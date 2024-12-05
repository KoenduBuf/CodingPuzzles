public class _15__LatticePaths {
    public static void main(String[] args) {
        System.out.println(solve(20, 20));
    }

    public static long solve(int w, int h) {
        return solve(0, 0, w, h);
    }
    private static long solve(int atX, int atY, int w, int h) {
        if(atY == h || atX == w) return 1;

        long toRight = solve(atX + 1, atY, w, h);
        long toDown = solve(atX, atY + 1, w, h);
//        System.out.println(atX + " " + atY + " " + toRight + " " + toDown);
        return toRight + toDown;
    }
}
