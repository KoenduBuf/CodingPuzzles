import java.math.BigInteger;

public class _16__PowerDigitSum {
    public static void main(String[] args) {
        BigInteger bi = new BigInteger("2").pow(1000);
        System.out.println(bi.toString());
        long sum = 0;
        for (char c : bi.toString().toCharArray()) {
            sum += (byte)(c - 48);
        }
        System.out.println(sum);
    }
}
