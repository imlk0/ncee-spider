package top.imlk.ncee.query;

import top.imlk.ncee.abstracts.LogableRunnable;
import top.imlk.ncee.abstracts.StopAbleBlockingQueue;
import top.imlk.ncee.message.Receiver;
import top.imlk.ncee.message.Sender;

public class ResultSpliter extends LogableRunnable implements Sender, Receiver {

    private StopAbleBlockingQueue<Student> failedQueryStudentsQueue;

    private StopAbleBlockingQueue<Student> queryedStudentQueue;

    private StopAbleBlockingQueue<Student> writeOutStudentQueue;


    public ResultSpliter(StopAbleBlockingQueue<Student> failedQueryStudentsQueue, StopAbleBlockingQueue<Student> queryedStudentQueue, StopAbleBlockingQueue<Student> writeOutStudentQueue) {
        this.failedQueryStudentsQueue = failedQueryStudentsQueue;
        this.queryedStudentQueue = queryedStudentQueue;
        this.writeOutStudentQueue = writeOutStudentQueue;
    }


    @Override
    public void doRun() {

        this.failedQueryStudentsQueue.registerSender(this);
        this.queryedStudentQueue.registerReceiver(this);
        this.writeOutStudentQueue.registerSender(this);


        while (true) {

            Student student = null;
            try {
                try {

                    if ((student = determineReceive(queryedStudentQueue, 7000)) == null) {
                        break;
                    }


                } catch (InterruptedException e) {
                    logger.info("{} 遭遇中断", this);
                    break;
                }


                try {

                    QueryHelper.splitQueryJsonResult(student, student.query_result_body);

                } catch (Throwable e) {
                    logger.error("解析query结果JSON时出现异常 Student:" + student, e);
                }

                if (student._score_str == null && student.failedCount < Queryer.QUERY_RETRY_TIME) {
                    student.failedCount++;
                    failedQueryStudentsQueue.put(student);

//                    logger.debug("失败 body：{}", student.query_result_body);
                    logger.info("重试 失败次数{} Student：{}", student.failedCount, student);

                } else {
                    if (student._score_str != null) {
                        logger.info("成功解析出成绩 Student：{}", student);
                    }
                    writeOutStudentQueue.put(student);
                }

            } catch (InterruptedException e) {
                break;
            }
        }


        this.failedQueryStudentsQueue.unregisterSender(this);
        this.queryedStudentQueue.unregisterReceiver(this);
        this.writeOutStudentQueue.unregisterSender(this);
    }


    @Override
    public boolean willBeMoreData() {
        return true;
    }

    @Override
    public boolean needMoreData() {
        return queryedStudentQueue.willBeMoreData();
    }
}
