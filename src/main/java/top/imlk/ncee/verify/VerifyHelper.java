package top.imlk.ncee.verify;

import com.alibaba.fastjson.JSONObject;
import okhttp3.*;
import org.apache.commons.io.FileUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.imageio.ImageIO;
import javax.script.Invocable;
import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;
import javax.script.ScriptException;
import java.awt.image.BufferedImage;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.util.Arrays;
import java.util.Base64;
import java.util.Random;
import java.util.concurrent.TimeUnit;

public class VerifyHelper {
    public static Logger logger = LoggerFactory.getLogger(VerifyHelper.class);

    private volatile OkHttpClient verifySiteClient;

    public OkHttpClient getVerifySiteClient() {
        if (verifySiteClient == null) {
            synchronized (this) {
                if (verifySiteClient == null) {
                    verifySiteClient = new OkHttpClient.Builder()
                            .connectTimeout(5000, TimeUnit.MILLISECONDS)
                            .readTimeout(10000, TimeUnit.MILLISECONDS)
                            .writeTimeout(10000, TimeUnit.MILLISECONDS)
//                            .addInterceptor(new LogInterceptor())
                            .build();
                }
            }
        }
        return verifySiteClient;
    }

    private static Headers headers = new Headers.Builder()
            .add("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0")
            .add("Accept", "*/*")
            .add("Accept-Language", "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2")
            .add("Accept-Encoding", "gzip, deflate")
            .add("Referer", "http://gkcf.jxedu.gov.cn/")
            .add("Connection", "keep-alive")
            .add("Pragma", "no-cache")
            .add("Cache-Control", "no-cache")
            .add("Host", "171.34.169.85")
            .build();

    private static Random sRandom = new Random();

    public Response doCheckCodeReq(CrackResult crackResult, Response lastResp, String ip) throws IOException {


        String fakeData = generateFakeData(crackResult);

        if (fakeData == null) {
            return null;
        }

        HttpUrl httpUrl = new HttpUrl.Builder()
                .scheme("http")
                .host(ip)
                .addPathSegments("api/checkcode")
                .addQueryParameter("callback", lastResp.request().url().queryParameter("callback"))
                .addQueryParameter("data", fakeData)
                .addQueryParameter("type", "0")
                .addQueryParameter("_", lastResp.request().url().queryParameter("_"))
                .build();

        Request request = new Request.Builder()
                .headers(headers)
                .header("Host", ip)
                .url(httpUrl)
                .get()
                .build();

        return this.getVerifySiteClient().newCall(request).execute();

    }


    private static ScriptEngineManager manager = new ScriptEngineManager();
    private static ScriptEngine scriptEngine = manager.getEngineByExtension("js");

    static {
        try {
            scriptEngine.eval(FileUtils.readFileToString(new File(ClassLoader.getSystemClassLoader().getResource("lz-string.min.js").getFile()), "UTF-8"));

        } catch (ScriptException | IOException e) {
            logger.error("载入脚本出错", e);
        }
    }

    private static Object lZStringObject = scriptEngine.get("LZString");


    public static String generateFakeData(CrackResult crackResult) {
        JSONObject jsonObject = new JSONObject();

        jsonObject.put("Id", crackResult.regionalVerifyImage.Id);
        jsonObject.put("point", crackResult.resultX);
        jsonObject.put("timespan", 1343 + ((int) (Math.random() * 40)) - 20);
        jsonObject.put("datelist", generateDatelist(crackResult));

        String jsonStr = jsonObject.toJSONString();


        try {
            if (scriptEngine instanceof Invocable) {


                Invocable invocable = ((Invocable) scriptEngine);

                Object invokeResult = invocable.invokeMethod(lZStringObject, "compressToEncodedURIComponent", jsonStr);

//                logger.debug("invoke LZString.compressToEncodedURIComponent Result:" + invokeResult);

                return invokeResult.toString();

            } else {
                logger.error("此脚本引擎不支持调用函数");
            }


        } catch (ScriptException | NoSuchMethodException e) {
            logger.error("执行脚本出错", e);
        }


        return null;
    }


    private static final int[] pList = {
            2,
            4,
            9,
            13,
            14,
            18,
            25,
            37,
            47,
            56,
            69,
            77,
            79,
            88,
            98,
            100,
            104,
            107,
            112,
            121,
            127,
            130,
            131,
            133,
            134,
            137,
            138,
            142,
            142,
            143,
            145,
            146,
            147,
            150,
            153,
            155,
            157,
            158,
            158,
            160,

    };

    private static final long[] tList = {
            0,
            9,
            42,
            58,
            73,
            90,
            106,
            123,
            139,
            156,
            174,
            189,
            209,
            225,
            243,
            258,
            276,
            292,
            307,
            328,
            344,
            356,
            373,
            390,
            405,
            424,
            446,
            478,
            509,
            526,
            588,
            604,
            673,
            757,
            790,
            906,
            958,
            1057,
            1075,
            1106,

    };

    public static String generateDatelist(CrackResult crackResult) {
        int point = crackResult.resultX;

        StringBuilder stringBuilder = new StringBuilder();
        long startTime = System.currentTimeMillis();
        for (int i = 0; i < pList.length; ++i) {
            stringBuilder.append(pList[i] * point / (200 - 40));
            stringBuilder.append(",");
            stringBuilder.append(tList[i] + startTime);
            stringBuilder.append("|");
        }

        if (pList.length > 0) {
            stringBuilder.deleteCharAt(stringBuilder.length() - 1);
        }


        return stringBuilder.toString();
    }


    public Response doGetCodeReq(String ip) throws IOException {

//        GET http://171.34.169.85/api/getcode?callback=jQuery1110043457577585351204_1536923045598&spec=200*100&type=0&_=1536923045599 HTTP/1.1
        HttpUrl httpUrl = new HttpUrl.Builder()
                .scheme("http")
                .host(ip)
                .addPathSegments("api/getcode")
                .addQueryParameter("callback", String.format("jQuery11100%017d_%d", sRandom.nextLong() % 100000000000000000L, System.currentTimeMillis()))
                .addQueryParameter("spec", "200*100")
                .addQueryParameter("type", "0")
                .addQueryParameter("_", "" + System.currentTimeMillis())
                .build();

        Request request = new Request.Builder()
                .headers(headers)
                .header("Host", ip)
                .url(httpUrl)
                .get()
                .build();

        return this.getVerifySiteClient().newCall(request).execute();

    }


    public static JSONObject parseJQueryRespJsonObj(String body) throws RuntimeException {

//        logger.info(body);

        int index = 0;
        if (body == null || "".equals(body) || ((index = body.indexOf("{")) == -1)) {

            throw new RuntimeException("invaild response: " + body);
        }
        return JSONObject.parseObject(body.substring(index, body.lastIndexOf("}") + 1));
    }


    public static String parseToken(JSONObject jsonObject) {
        return jsonObject.getString("token");
    }


    /**
     * function (result) {
     * Id = result['Id'];
     * if (result['state'] === -1) {
     * return;
     * }
     * var errcode = result['errcode'];
     * if (errcode !== 0) {
     * document.getElementById(__codediv).innerHTML =
     * "<span style='color:red'>\u9a8c\u8bc1\u7801\u83b7\u53d6\u5931\u8d25\u002c"
     * + result['errmsg'] + "</span>";
     * }
     * var yvalue = result['y'], smallImg = result['smallImg'], array = result['array'], normalImg = result['normalImg'];
     * imgx = result['imgx'];
     * imgy = result['imgy'];
     * $(".cut_bg").css("background-image", "url(" + normalImg + ")");
     * $("#xy_img").css("background-image", "url(" + smallImg + ")");
     * $("#xy_img").css("top", yvalue);
     * $("#drag").css("width", imgx);
     * $("#drag .drag_text").css("width", imgx);
     * $(".cut_bg").css("width", imgx / 10);
     * $(".cut_bg").css("height", imgy / 2);
     * $(".refesh_bg").show();
     * $(".refesh_bg").css("left", imgx - 20);
     * $(".refesh_bg").css("top", imgy - 20);
     * var bgarray = array.split(',');
     * //还原图片
     * var _cutX = imgx / 10;
     * var _cutY = imgy / 2;
     * for (var i = 0; i < bgarray.length; i++) {
     * var num = indexOf(bgarray, i.toString()); //第i张图相对于混淆图片的位置为num
     * var x = 0, y = 0;
     * //还原前偏移
     * y = i > 9 ? -_cutY : 0;
     * x = i > 9 ? (i - 10) * -_cutX : i * -_cutX;
     * //当前y轴偏移量
     * if (num > 9 && i < 10) y = y - _cutY;
     * if (i > 9 && num < 10) y = y + _cutY;
     * //当前x轴偏移量
     * x = x + (num - i) * -_cutX;
     * //显示第i张图片
     * $("#bb" + i).css("background-position", x + "px " + y + "px");
     * }
     * //完成,移除提示
     * $(".vcode-hints").remove();
     * });
     */

    public static VerifyImage parseVerifyImage(JSONObject jsonObject) {


        String smallStr = jsonObject.getString("small");
        String normalStr = jsonObject.getString("normal");

        int imgX = jsonObject.getIntValue("imgx");
        int imgY = jsonObject.getIntValue("imgy");

        int y = jsonObject.getIntValue("y");
        int Id = jsonObject.getIntValue("Id");

        int _cutX = imgX / 10;
        int _cutY = imgY / 2;

        byte[] normalByte = decodeBase64Image(normalStr);
        byte[] smallByte = decodeBase64Image(smallStr);

        String arrayStr = jsonObject.getString("array");

//        try {
//            FileUtils.writeByteArrayToFile(new File("smallImg.jpg"), smallByte);
//            FileUtils.writeByteArrayToFile(new File("normalImg.jpg"), normalByte);
//        } catch (IOException e) {
//            e.printStackTrace();
//        }


        try {

            BufferedImage sourceImage = ImageIO.read(new ByteArrayInputStream(normalByte));

            BufferedImage resultImage = new BufferedImage(imgX, imgY, BufferedImage.TYPE_INT_RGB);


            int[] posArray = Arrays.stream(arrayStr.split(","))
                    .mapToInt(Integer::parseInt).toArray();

            int[] buffer = null;
            int index = 0;

            for (int pos : posArray) {

                int _y = -(pos / 10) * _cutY;
                int _x = (pos % 10) * _cutX;

                if (index > 9 && pos < 10) _y = _y + _cutY;
                if (pos > 9 && index < 10) _y = _y - _cutY;

                _x = _x + (index - pos) * _cutX;

                //显示第pos张图片

//                logger.debug("sourceImage.getRGB() " + Arrays.asList((x % imgX + imgX) % imgX, (y % imgY + imgY) % imgY, _cutX, _cutY, buffer, 0, _cutX));
                buffer = sourceImage.getRGB((_x % imgX + imgX) % imgX, (_y % imgY + imgY) % imgY, _cutX, _cutY, buffer, 0, _cutX);
//                logger.debug("resultImage.setRGB() " + Arrays.asList((pos % 10) * _cutX, (pos / 10) * _cutY, _cutX, _cutY, buffer, 0, _cutX));
                resultImage.setRGB((pos % 10) * _cutX, (pos / 10) * _cutY, _cutX, _cutY, buffer, 0, _cutX);

                index++;
            }

            ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();

            ImageIO.write(resultImage, "JPEG", byteArrayOutputStream);


            VerifyImage verifyImage = new VerifyImage();
            verifyImage.imgX = imgX;
            verifyImage.imgY = imgY;
            verifyImage.y = y;
            verifyImage.normalImg = byteArrayOutputStream.toByteArray();
            verifyImage.smallImg = smallByte;
            verifyImage.Id = Id;


            return filteBadData(verifyImage);

        } catch (IOException e) {
            e.printStackTrace();
        }

        return null;
    }

    public static VerifyImage filteBadData(VerifyImage verifyImage) {
        if (verifyImage.imgX == 0 || verifyImage.imgY == 0 || verifyImage.normalImg == null || verifyImage.smallImg == null) {
            return null;
        }

        return verifyImage;
    }

    public static byte[] decodeBase64Image(String str) {

        return Base64.getDecoder().decode(str.substring("data:image/jpg;base64,".length(), str.length()));

    }

}
