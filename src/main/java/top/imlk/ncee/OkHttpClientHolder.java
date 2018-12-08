package top.imlk.ncee;

import okhttp3.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.concurrent.TimeUnit;

public class OkHttpClientHolder {

    private static OkHttpClient verifySiteClient;

    public static OkHttpClient getVerifySiteClient() {

        if (verifySiteClient == null) {
            synchronized (OkHttpClientHolder.class) {
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


    private static OkHttpClient querySiteClient;

    public static OkHttpClient getQuerySiteClient() {

        if (querySiteClient == null) {
            synchronized (OkHttpClientHolder.class) {
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


    static class LogInterceptor implements Interceptor {
        public static Logger logger = LoggerFactory.getLogger(LoggerFactory.class);


        @Override
        public Response intercept(Chain chain) throws IOException {

            Request request = chain.request();
            logger.info(request.toString());

            Response response = null;
            response = chain.proceed(request);

            logger.info(response.toString());


            return response;
        }
    }
}
