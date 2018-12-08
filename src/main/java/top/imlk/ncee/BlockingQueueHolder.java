package top.imlk.ncee;

import top.imlk.ncee.abstracts.StopAbleBlockingQueue;
import top.imlk.ncee.query.Student;

public class BlockingQueueHolder {
    public final StopAbleBlockingQueue<Student> readInStudentsQueue = new StopAbleBlockingQueue<>(100);
    public final StopAbleBlockingQueue<String> queryTokenQueue = new StopAbleBlockingQueue<>(20);
    public final StopAbleBlockingQueue<Student> queryedStudentQueue = new StopAbleBlockingQueue<>(100);

    public final StopAbleBlockingQueue<Student> writeOutStudentQueue = new StopAbleBlockingQueue<>(100);


    public final StopAbleBlockingQueue<Student> failedQueryStudentsQueue = new StopAbleBlockingQueue<>(100);


}
