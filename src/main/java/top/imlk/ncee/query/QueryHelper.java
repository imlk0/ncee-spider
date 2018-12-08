package top.imlk.ncee.query;

import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONException;
import com.alibaba.fastjson.JSONObject;
import okhttp3.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.concurrent.TimeUnit;

public class QueryHelper {

    public static Logger logger = LoggerFactory.getLogger(QueryHelper.class);


    private OkHttpClient querySiteClient;

    public OkHttpClient getQuerySiteClient() {

        if (querySiteClient == null) {
            synchronized (this) {
                if (querySiteClient == null) {

                    CookieJar cookieJar = new CookieJar() {
                        private HashMap<String, List<Cookie>> cookieStore = new HashMap<String, List<Cookie>>();

                        @Override
                        public void saveFromResponse(HttpUrl url, List<Cookie> cookies) {
                            cookieStore.put(url.host(), cookies);
                        }

                        @Override
                        public List<Cookie> loadForRequest(HttpUrl url) {
                            List<Cookie> cookies = cookieStore.get(url.host());
                            return cookies != null ? cookies : new ArrayList<Cookie>();
                        }
                    };

                    querySiteClient = new OkHttpClient.Builder()
                            .connectTimeout(5000, TimeUnit.MILLISECONDS)
                            .readTimeout(10000, TimeUnit.MILLISECONDS)
                            .writeTimeout(10000, TimeUnit.MILLISECONDS)
                            .cookieJar(cookieJar)
//                            .addInterceptor(new LogInterceptor())
                            .build();
                }
            }
        }

        return querySiteClient;
    }


    private static Headers headers = new Headers.Builder()
            .add("Host", "gkcf.jxedu.gov.cn")
            .add("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0")
            .add("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
            .add("Accept-Language", "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2")
            .add("Accept-Encoding", "gzip, deflate")
            .add("Referer", "http://gkcf.jxedu.gov.cn/")
            .add("Content-Type", "application/x-www-form-urlencoded")
//            .add("Content-Length", "251")
//            .add("Cookie", "state=1; .AspNetCore.Antiforgery.Uoi1ttXMTU4=CfDJ8GaVu4zpWI1AvX5NAmHQNCBWKbFabcmUDv5ypdpoxwMrStefX8-_uuI_5hhOUFOw8xuA5i4FDPKqJffjpPLJsGs_AxpJabyVZNIYsssMnRukF3z_9OzMAAQXKA5vTKYL6otj2kcFWhPIRibqQupiYYw; user=null; smallscore=null; luqu=null")
            .add("Connection", "keep-alive")
            .add("Upgrade-Insecure-Requests", "1")
            .build();


    public volatile String __RequestVerificationToken = "CfDJ8GaVu4zpWI1AvX5NAmHQNCBmptVyMH2JoYjwqpD-qL1sqGZG-1nD5kK9Af-PQXQkeFjRofJcC2YKm0vht_fLUOpH2J94BTY5TB46-sKAdKGMHKClGZIVySdnqR74qEuqAgu6Dux_UQsiX0dpOCoispA";

    public Response doQueryReq(Student student) throws IOException {

        HttpUrl httpUrl = new HttpUrl.Builder()
                .scheme("http")
                .host("gkcf.jxedu.gov.cn")
                .build();

        String sfzh = String.valueOf(student.sfzh);
        sfzh = sfzh.substring(sfzh.length() - 4, sfzh.length());
        Request request = new Request.Builder()
                .headers(headers)
                .url(httpUrl)
                .post(new FormBody.Builder()
                        .add("key1", String.valueOf(student.ksh))
                        .add("key2", sfzh)
                        .add("token", student.token)
                        .add("__RequestVerificationToken", __RequestVerificationToken)
                        .build()
                )
                .build();

        Response queryResp = getQuerySiteClient().newCall(request).execute();

        logger.debug("query请求响应 {}", queryResp);

        return queryResp;
    }

    public Response doUpdateCSRFTokenReq() throws IOException {

        HttpUrl httpUrl = new HttpUrl.Builder()
                .scheme("http")
                .host("gkcf.jxedu.gov.cn")
                .build();

        Request request = new Request.Builder()
                .headers(headers)
                .removeHeader("Cookie")
                .url(httpUrl)
                .get()
                .build();

        return getQuerySiteClient().newCall(request).execute();

    }

    public static final String __RequestVerificationToken_NAME = "__RequestVerificationToken";

    public static String parseCSRFToken(String body) {
//                        <input name="__RequestVerificationToken" type="hidden" value="CfDJ8BA86aQelU5FrJ8CexiSOkB7usAF_EC6xOExYVQGPHHWVGs-zThDD0H-Sf5RGxDcEyY3OpiST7EOmE2IxM71Y3R4oUq8SOJAxeGg1yKc6kgeJjylaE1B_UMfDF52mGA1hNlnudnCjGeiXFtYqPoIS_k" /></form>

        String csrfToken = null;
        int start, end;
        start = body.indexOf(__RequestVerificationToken_NAME);
        if (start != -1) {
            start = start + __RequestVerificationToken_NAME.length();

            start = body.indexOf("value=\"", start);
            start = start + "value=\"".length();
            end = body.indexOf("\"", start);

            csrfToken = body.substring(start, end);
        }
        if (csrfToken == null || "".equals(csrfToken)) {

            logger.error("解析CSRFToken失败，未找到目标在响应body中");
            return null;
        } else {
            logger.error("解析出新的CSRFToken：{}", csrfToken);
            return csrfToken;
        }
    }

    private static final String score_HEAD = "var _score = '";
    private static final String scores_HEAD = "var _scores = '";
    private static final String luqu_HEAD = "var _luqu = '";


    public static void splitQueryJsonResult(Student student, String str) {

        if (str == null || "".equals(str)) {
            return;
        }


        int start, end;

        try {
            start = str.indexOf(score_HEAD);
            if (start != -1) {
                start = start + score_HEAD.length();
                end = str.indexOf('\'', start);
                student._score_str = str.substring(start, end).toLowerCase();
                student._score_json = JSONObject.parseObject(student._score_str);// _score字段需要转小写

            }


            start = str.indexOf(scores_HEAD);
            if (start != -1) {
                start = start + scores_HEAD.length();
                end = str.indexOf('\'', start);
                student._scores_str = str.substring(start, end);
                student._scores_json = JSONArray.parseArray(student._scores_str);
            }


            start = str.indexOf(luqu_HEAD);
            if (start != -1) {
                start = start + luqu_HEAD.length();
                end = str.indexOf('\'', start);
                student._luqu_str = str.substring(start, end);
                student._luqu_json = JSONObject.parseObject(student._luqu_str);
            }

        } catch (JSONException e) {
            logger.error("转换JSON出错 " + student + "\n原文档：" + student.query_result_body, e);
        }

    }
}
