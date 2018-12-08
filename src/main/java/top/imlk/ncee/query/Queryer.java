package top.imlk.ncee.query;

import okhttp3.Response;
import top.imlk.ncee.abstracts.LogableRunnable;
import top.imlk.ncee.abstracts.StopAbleBlockingQueue;
import top.imlk.ncee.message.Receiver;
import top.imlk.ncee.message.Sender;

import java.io.IOException;

public class Queryer extends LogableRunnable implements Receiver, Sender {

    public static final int QUERY_RETRY_TIME = 5;

    private StopAbleBlockingQueue<String> queryTokenQueue;

    private StopAbleBlockingQueue<Student> toQueryeStudentsQueue;

    private StopAbleBlockingQueue<Student> queryedStudentQueue;

    private QueryHelper queryHelper = new QueryHelper();


    public Queryer(StopAbleBlockingQueue<String> queryTokenQueue, StopAbleBlockingQueue<Student> toQueryeStudentsQueue, StopAbleBlockingQueue<Student> queryedStudentQueue) {
        this.queryTokenQueue = queryTokenQueue;
        this.toQueryeStudentsQueue = toQueryeStudentsQueue;
        this.queryedStudentQueue = queryedStudentQueue;
    }

    @Override
    public void doRun() {
        this.queryTokenQueue.registerReceiver(this);
        this.toQueryeStudentsQueue.registerReceiver(this);
        this.queryedStudentQueue.registerSender(this);


        while (true) {

            try {

                String token = queryTokenQueue.take();

                Student student;

                try {
                    if ((student = this.determineReceive(toQueryeStudentsQueue, 7000)) == null) {
                        break;
                    }
                } catch (InterruptedException e) {
                    logger.info("{} 遭遇中断", this);
                    break;
                }

                student.token = token;

                String queryBody = null;

                try {
                    queryBody = doQuery(student);

                } catch (Throwable e) {
                    logger.error("query时出现异常 Student:" + student, e);
                }

                student.query_result_body = queryBody;

                try {
                    queryedStudentQueue.put(student);

                } catch (InterruptedException e) {
                    logger.info("{} 遭遇中断", this);
                    break;
                }


            } catch (InterruptedException e) {
                break;
            }
        }


        this.queryTokenQueue.unregisterReceiver(this);
        this.toQueryeStudentsQueue.unregisterReceiver(this);
        this.queryedStudentQueue.unregisterSender(this);
    }

    public String doQuery(Student student) throws IOException {

        Response queryResp = queryHelper.doQueryReq(student);

        String queryBody = queryResp.body().string();

        if (queryResp.code() == 500 || queryResp.code() == 400 || queryBody == null || "".equals(queryBody)) {
            logger.info("CSRFToken过期，尝试重新获取");
            Response updateCSRFTokenResp = queryHelper.doUpdateCSRFTokenReq();
            logger.info("获取新的CSRFToken的请求的响应 {}", updateCSRFTokenResp);
            String updateCSRFTokenBody = updateCSRFTokenResp.body().string();
//            logger.info("获取新的CSRFToken的请求的Body {}", updateCSRFTokenBody);
            String csrfToken = QueryHelper.parseCSRFToken(updateCSRFTokenBody);
            queryHelper.__RequestVerificationToken = csrfToken;

            queryResp = queryHelper.doQueryReq(student);
            queryBody = queryResp.body().string();

        }

        return queryBody;
    }

    @Override
    public boolean needMoreData() {
        return toQueryeStudentsQueue.willBeMoreData()
                && queryTokenQueue.willBeMoreData();
    }

    @Override
    public boolean willBeMoreData() {
        return toQueryeStudentsQueue.size() > 0;
//        return toQueryeStudentsQueue.willBeMoreData() || toQueryeStudentsQueue.size() > 0;// 考虑
    }
}
