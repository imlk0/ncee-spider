package top.imlk.ncee.verify;

import org.opencv.core.*;
import org.opencv.core.Point;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import top.imlk.ncee.OpenCVForm;

import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.*;

public class ImageMatcher {

    public static Logger logger = LoggerFactory.getLogger(ImageMatcher.class);

    static {
        System.loadLibrary(Core.NATIVE_LIBRARY_NAME);

    }

    private static final boolean SHOW_JFRAME = false;


    private static final int DEFAULT_METHOD_INDEX = 0;


    public static CrackResult match(VerifyImage verifyImage) throws IOException {


        CrackResult result = doMatchBy(verifyImage, DEFAULT_METHOD_INDEX);


        if (SHOW_JFRAME) {

            // 可视化匹配调试

            JFrame.setDefaultLookAndFeelDecorated(true);

            OpenCVForm openCVFormForm = new OpenCVForm();

            openCVFormForm.show();
            openCVFormForm.slider1.setValue(DEFAULT_METHOD_INDEX);

            openCVFormForm.slider1.addChangeListener((event) -> {
                try {

                    CrackResult crackResult = doMatchBy(verifyImage, matchMethods[openCVFormForm.slider1.getValue()]);

                    openCVFormForm.showCreckResult(crackResult);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            });

            openCVFormForm.showCreckResult(result);
        }

        return result;

    }

    private static final int[] matchMethods = {
            Imgproc.TM_SQDIFF,
            Imgproc.TM_SQDIFF_NORMED,
            Imgproc.TM_CCORR,
            Imgproc.TM_CCORR_NORMED,
            Imgproc.TM_CCOEFF,
            Imgproc.TM_CCOEFF_NORMED,

    };

    private static CrackResult doMatchBy(VerifyImage verifyImage, int match_method) throws IOException {


        // 载入验证码底图矩阵
        Mat srcImgMat = Imgcodecs.imdecode(new MatOfByte(verifyImage.normalImg), Imgcodecs.IMREAD_COLOR);

        // 载入小图并准备加水印
        BufferedImage smallBufferedImage = ImageIO.read(new ByteArrayInputStream(verifyImage.smallImg));

        // 加水印
        Graphics graphics = smallBufferedImage.getGraphics();
        graphics.setColor(new Color(0, 0, 0, 100));
        graphics.fillRect(0, 0, smallBufferedImage.getWidth(), smallBufferedImage.getHeight());
        graphics.dispose();

        // 生成加水印后的jpg图片数据
        ByteArrayOutputStream byteArray = new ByteArrayOutputStream();
        ImageIO.write(smallBufferedImage, "jpg", byteArray);
        byte[] crackedSmall = byteArray.toByteArray();

        //载入加水印后的小图矩阵
        // 由于原来的项目被魔改，水印方式已经更变，四周的一圈象素不是直接加灰度的，此处将匹配图缩小一圈
        Mat smallImgMat = Imgcodecs.imdecode(new MatOfByte(crackedSmall), Imgcodecs.IMREAD_COLOR);
        smallImgMat = smallImgMat.submat(1, smallImgMat.rows() - 1, 1, smallImgMat.cols() - 1);


        // match结果矩阵,这里只选择第y行开始的以提高速度
        Mat matchOutMat = new Mat();
        //由于匹配图缩小一圈，此处把匹配位置y+1以提升匹配成功率
        int matchSartRow = verifyImage.y + 1;
        Imgproc.matchTemplate(srcImgMat.submat(matchSartRow, matchSartRow + smallImgMat.rows(), 0, srcImgMat.cols()), smallImgMat, matchOutMat, match_method);


        //打印三个矩阵信息
//        System.out.println("srcImgMat:" + srcImgMat.cols() + " " + srcImgMat.rows());
//        System.out.println("tempImgMat:" + smallImgMat.cols() + " " + smallImgMat.rows());
//        System.out.println("resultMat:" + matchOutMat.cols() + " " + matchOutMat.rows());
//        System.out.println(matchOutMat.dump());
//        System.out.println("\n\n\n");


        // 归一化，将数据归一到alpha和beta之间
        Core.normalize(matchOutMat, matchOutMat, 0, 1, Core.NORM_MINMAX, -1);
//        System.out.println(matchOutMat.dump());

        // 求矩阵中的最大最小值位置及其值
        Core.MinMaxLocResult minMaxLocResult = Core.minMaxLoc(matchOutMat);


        // 根据不同的match算法选出合适的点
        org.opencv.core.Point aimPoint;

        if (match_method == Imgproc.TM_SQDIFF || match_method == Imgproc.TM_SQDIFF_NORMED) {
            aimPoint = minMaxLocResult.minLoc;
        } else {
            aimPoint = minMaxLocResult.maxLoc;
        }


        // 函数运行结果
        CrackResult crackResult = new CrackResult();

        crackResult.regionalVerifyImage = verifyImage;

        crackResult.resultX = ((int) aimPoint.x);


        if (SHOW_JFRAME) {

            crackResult.crackedNormalImg = verifyImage.normalImg;

            crackResult.crackedSmallImg = crackedSmall;

            //准备crack标记结果矩阵
            Mat resultVisualMat = new Mat();
            srcImgMat.copyTo(resultVisualMat);


            // 在图上标记match点
            Imgproc.rectangle(resultVisualMat, new org.opencv.core.Point(aimPoint.x, aimPoint.y + matchSartRow), new Point(aimPoint.x + smallImgMat.cols(), matchSartRow + aimPoint.y + smallImgMat.rows()), new Scalar(0, 0, 255), 2, 8, 0);

            MatOfByte byteMat;

            Imgcodecs.imencode(".jpg", resultVisualMat, byteMat = new MatOfByte());

            crackResult.crackedResultImg = byteMat.toArray();

        }

//        logger.info("crackResult:" + crackResult);

        return crackResult;
    }

}
