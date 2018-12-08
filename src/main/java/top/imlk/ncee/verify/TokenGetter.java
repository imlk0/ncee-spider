package top.imlk.ncee.verify;

import com.alibaba.fastjson.JSONObject;
import okhttp3.Response;
import top.imlk.ncee.abstracts.LogableRunnable;
import top.imlk.ncee.abstracts.StopAbleBlockingQueue;
import top.imlk.ncee.message.Sender;

import java.io.IOException;

public class TokenGetter extends LogableRunnable implements Sender {


    private VerifyHelper verifyHelper = new VerifyHelper();

    public TokenGetter(StopAbleBlockingQueue<String> queryTokenQueue) {
        this.queryTokenQueue = queryTokenQueue;
    }

    private StopAbleBlockingQueue<String> queryTokenQueue;


    @Override
    public void doRun() {

        this.queryTokenQueue.registerSender(this);


        while (true) {

            try {
                String token = getToken();

                if (token == null || "".equals(token)) {

                    logger.error("获取到空token，先停一秒缓一缓");
                    Thread.sleep(1000);
                } else {

                    try {

                        if (!this.determineSend(queryTokenQueue, token, 7000)) {
                            break;
                        }

                    } catch (InterruptedException e) {
                        logger.info("{} 遭遇中断", this);
                        break;
                    }

                }

            } catch (InterruptedException e) {
                break;
            } catch (Throwable e) {
                logger.error("获取token时发生异常", e);
            }

        }

        this.queryTokenQueue.unregisterSender(this);

    }


    public String getToken() throws IOException {

        String ip = IPPool.randomIP();

        Response getCodeResp = verifyHelper.doGetCodeReq(ip);
        String getCodeBody = getCodeResp.body().string();
        JSONObject getCodeJsonObj = VerifyHelper.parseJQueryRespJsonObj(getCodeBody);
        VerifyImage verifyImage = VerifyHelper.parseVerifyImage(getCodeJsonObj);
        CrackResult crackResult = ImageMatcher.match(verifyImage);
        Response checkCodeResp = verifyHelper.doCheckCodeReq(crackResult, getCodeResp, ip);
        String checkCodeBody = checkCodeResp.body().string();
        JSONObject checkCodeJsonObj = VerifyHelper.parseJQueryRespJsonObj(checkCodeBody);
        String token = VerifyHelper.parseToken(checkCodeJsonObj);

        logger.debug("{} 获取到token：{}", this, token);

        return token;
    }

    @Override
    public boolean willBeMoreData() {
        return true;
    }
}
