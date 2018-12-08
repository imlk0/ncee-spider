package top.imlk.ncee;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import top.imlk.ncee.input.ExcelReader;
import top.imlk.ncee.output.ExcelWriter;
import top.imlk.ncee.query.Queryer;
import top.imlk.ncee.query.ResultSpliter;
import top.imlk.ncee.verify.*;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class Launcher {

    public static Logger logger = LoggerFactory.getLogger(Launcher.class);


    public static void main(String[] args) {

        BlockingQueueHolder blockingQueueHolder = new BlockingQueueHolder();


//        ExecutorService executors = Executors.newCachedThreadPool();


        String sourceFile = "测试数据.xlsx";


        // 学生读入
        new Thread(new ExcelReader(sourceFile, blockingQueueHolder.readInStudentsQueue)).start();

        //token获取
        new Thread(new TokenGetter(blockingQueueHolder.queryTokenQueue)).start();
        new Thread(new TokenGetter(blockingQueueHolder.queryTokenQueue)).start();
        new Thread(new TokenGetter(blockingQueueHolder.queryTokenQueue)).start();
        new Thread(new TokenGetter(blockingQueueHolder.queryTokenQueue)).start();

        //成绩查询
        new Thread(new Queryer(blockingQueueHolder.queryTokenQueue, blockingQueueHolder.readInStudentsQueue, blockingQueueHolder.queryedStudentQueue)).start();
        new Thread(new Queryer(blockingQueueHolder.queryTokenQueue, blockingQueueHolder.readInStudentsQueue, blockingQueueHolder.queryedStudentQueue)).start();
        new Thread(new Queryer(blockingQueueHolder.queryTokenQueue, blockingQueueHolder.readInStudentsQueue, blockingQueueHolder.queryedStudentQueue)).start();
        new Thread(new Queryer(blockingQueueHolder.queryTokenQueue, blockingQueueHolder.readInStudentsQueue, blockingQueueHolder.queryedStudentQueue)).start();
        new Thread(new Queryer(blockingQueueHolder.queryTokenQueue, blockingQueueHolder.readInStudentsQueue, blockingQueueHolder.queryedStudentQueue)).start();
        new Thread(new Queryer(blockingQueueHolder.queryTokenQueue, blockingQueueHolder.readInStudentsQueue, blockingQueueHolder.queryedStudentQueue)).start();
        new Thread(new Queryer(blockingQueueHolder.queryTokenQueue, blockingQueueHolder.readInStudentsQueue, blockingQueueHolder.queryedStudentQueue)).start();

        //失败重试
        new Thread(new Queryer(blockingQueueHolder.queryTokenQueue, blockingQueueHolder.failedQueryStudentsQueue, blockingQueueHolder.queryedStudentQueue)).start();
        new Thread(new Queryer(blockingQueueHolder.queryTokenQueue, blockingQueueHolder.failedQueryStudentsQueue, blockingQueueHolder.queryedStudentQueue)).start();
//        new Thread(new Queryer(blockingQueueHolder.queryTokenQueue, blockingQueueHolder.failedQueryStudentsQueue, blockingQueueHolder.queryedStudentQueue)).start();

        //结果解析
        new Thread(new ResultSpliter(blockingQueueHolder.failedQueryStudentsQueue, blockingQueueHolder.queryedStudentQueue, blockingQueueHolder.writeOutStudentQueue)).start();
        new Thread(new ResultSpliter(blockingQueueHolder.failedQueryStudentsQueue, blockingQueueHolder.queryedStudentQueue, blockingQueueHolder.writeOutStudentQueue)).start();
        new Thread(new ResultSpliter(blockingQueueHolder.failedQueryStudentsQueue, blockingQueueHolder.queryedStudentQueue, blockingQueueHolder.writeOutStudentQueue)).start();

        //文件写出
        new Thread(new ExcelWriter(blockingQueueHolder.writeOutStudentQueue, String.format("ResultWB_%d.xls", System.currentTimeMillis()))).start();




    }


}
