package top.imlk.ncee.verify;

import java.util.Arrays;

public class CrackResult {

    VerifyImage regionalVerifyImage;
    int resultX;

    public byte[] crackedNormalImg;

    public byte[] crackedSmallImg;

    public byte[] crackedResultImg;

    @Override
    public String toString() {
        return "CrackResult{" +
                "regionalVerifyImage=" + regionalVerifyImage +
                ", resultX=" + resultX +
                ", crackedNormalImg=" + Arrays.toString(crackedNormalImg) +
                ", crackedSmallImg=" + Arrays.toString(crackedSmallImg) +
                ", crackedResultImg=" + Arrays.toString(crackedResultImg) +
                '}';
    }
}
