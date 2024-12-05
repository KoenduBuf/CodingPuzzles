public class Friendly10Substrings {
    public static void main(String[] args) {
        long startTime = System.currentTimeMillis();


//        System.out.println(isFriendly10SubString(new BigInteger("92546")));
//        System.out.println(T(new BigInteger("5")));
//        System.out.println(Integer.MAX_VALUE);
//        System.out.println(T(0,1000000000L));
//        System.out.println(isFriendly10SubString(String.valueOf(50050)));

        System.out.println(isFriendly10SubString("1810000000000000000000000000000000000000000000000000000000000000000000000000000010"));

//        System.out.println(matrixRow(100000000));
//        System.out.println(sumArr(preCalcMatrix[5]));



        System.out.println("Took: " + (System.currentTimeMillis() - startTime) + " ms");
    }

    private static int[][] preCalcMatrix = new int[][]{
            {9,         11,         10,         9,          8,          7,          6,          5,          4,          3},     //last 2 digits, assuming 0, 1, 2 etc as 3rd
            {72,        83,         72,         62,         53,         45,         38,         32,         27,         23},    //last 3 digits, assuming 0, 1, 2 etc as 4th
            {507,       571,        489,        418,        357,        305,        261,        224,        193,        167},   //last 4 digits, assuming 0, 1, 2 etc as 5th
            {3492,      3837,       3285,       2814,       2413,       2072,       1782,       1535,       1324,       1143},  //last 5 digits
            {23697,     25557,      21920,      18818,      16171,      13910,      11976,      10319,      8897,       7675},  //last 6 digits
            {158940,    169485,     145540,     125071,     107559,     92564,      79714,      68695,      59242,      51131},
            {1057941,   1121475,    963479,     828241,     712430,     613219,     528207,     455352,     392914,     339407}
    };

    private static long sumArr(long[] arr) {
        long res = 0;
        for (int i = 0; i < arr.length; i++) {
            res += arr[i];
        }
        return res;
    }

    private static long[] matrixRow(int x) {
        long[] res = new long[10];
        for (int i = 0; i < 10; i++) {
            res[i] = T(i*x, (i+1) * x);
        }
        return res;
    }

    //10^2: 9
    //10^3: 72
    //10^4: 507
//                            v4                      v5                  v6
    //10^5: 3492        (took 593 ms)               437 ms              0 ms
    //10^6: 23697       (took 4235 ms)              1906 ms             15 ms
    //10^7: 158940      (took 43621 ms)             10374 ms            94 ms
    //10^8: 1057941     (took 308320 ms)            72941 ms            531 ms
    //10^9: 7012665                                                     3656 ms
    //10^10: 46402069                                                   27377 ms

    private static long T(long till) {
        return T(18, till);
    }
    private static long T(long from, long till) {
        long res = 0;

        long toAdd = 1;
        for (long b = from; b <= till; b += toAdd) {
//            System.out.print("\r" + b + " of " + till);

            toAdd = isFriendly10SubString(String.valueOf(b));

            if (toAdd == -1) {
                toAdd = 1;
//                System.out.println(b);
                res++;
            }
            if (toAdd <= 0) {
//                System.out.println(" toadd was 0 " + b);
                toAdd = 1;
            }
        }
//        System.out.println();
        return res;
    }



    //assuming b.length <= 18
    //returns -1 for true, or > 0 to skip, or < 17 for where the mistake was
    private static long isFriendly10SubString(String b) {
        char[] chars = b.toCharArray();
        int clearedUntil = -1;
        for (int i = 0; i < chars.length; i++) {
            byte res = 0;
            for (int j = 0; j < chars.length - i; j++) {
                res += (byte) (chars[i+j] - 48);

                if (res == 10) {
                    int k;
                    for (k = 0; k < chars.length - i - j - 1; k++) {
                        if (chars[i+j+k+1] != '0') break;
                    }
                    clearedUntil = (i+j+k);
                    break;
                }

                if (res > 10) {
                    if (clearedUntil >= i) {
                        break;
                    } else {
                        int fromLeft = (chars.length - (i+j));
                        String sub = b.substring(i+j+1);
                        int last = sub.isEmpty() ? 0 : Integer.valueOf(sub);
                        if (fromLeft > 18) {
                            return -fromLeft;
                        }
                        return tenToPower(fromLeft) - (((chars[i+j] - 48)) * tenToPower(fromLeft-1)) - last;
                    }
                }
            }
        }
        if (clearedUntil == chars.length - 1) {
            return -1;
        }
        return 1;
    }
    private static long tenToPower(int i) {
        if (i < 0) System.out.println("WTF, i < 0");
        switch (i) {
            case 0:
                return 1;
            case 1:
                return 10;
            case 2:
                return 100;
            case 3:
                return 1000;
            case 4:
                return 10000;
            case 5:
                return 100000;
            case 6:
                return 1000000;
            case 7:
                return 10000000;
            case 8:
                return 100000000;
            case 9:
                return 1000000000;
            case 10:
                return 10000000000L;
            case 11:
                return 100000000000L;
            case 12:
                return 1000000000000L;
            case 13:
                return 10000000000000L;
            case 14:
                return 100000000000000L;
            case 15:
                return 1000000000000000L;
            case 16:
                return 10000000000000000L;
            case 17:
                return 100000000000000000L;
            default:
                return 1000000000000000000L;
        }
    }





    //just a list:
    //019
    //028
    //037
    //046
    //055
    //064
    //073
    //082
    //091
            // 9 in 0 - 100
    //109
    //118
    //127
    //136
    //145
    //154
    //163
    //172
    //181
    //190
    //191
            // 11 in 100 - 200 || 1x door 0 op index 1 || 1x door -1 van laatste getal
    //208
    //217
    //226
    //235
    //244
    //253
    //262
    //271
    //280
    //282
            // 10 in 200 - 300 || 1x door 2 -> 11
    //307
    //316
    //325
    //334
    //343
    //352
    //361
    //370
    //373
            // 9 in 300 - 400
    //406
    //415
    //424
    //433
    //442
    //451
    //460
    //464
            // 8 in 400 - 500
    //505
    //514
    //523
    //532
    //541
    //550
    //555
            // 7 in 500 - 600
    //604
    //613
    //622
    //631
    //640
    //646
            // 6 in 600 - 700
    //703
    //712
    //721
    //730
    //737
            // 5 in 700 - 800
    //802
    //811
    //820
    //828
            // 4 in 800 - 900
    //901
    //910
    //919
            // 3 in 900 - 1000


    //char to number = char - 48
}
