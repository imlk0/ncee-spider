package top.imlk.ncee.verify;

public class IPPool {
    private static final String[] pool = {
            "171.34.169.85",
    };


    public static String randomIP() {
        return pool[((int) (Math.random() * pool.length))];
    }

}
