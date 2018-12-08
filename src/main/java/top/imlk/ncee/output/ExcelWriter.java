package top.imlk.ncee.output;

import org.apache.commons.io.FileUtils;
import org.apache.poi.hssf.usermodel.HSSFWorkbook;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;
import top.imlk.ncee.abstracts.LogableRunnable;
import top.imlk.ncee.abstracts.StopAbleBlockingQueue;
import top.imlk.ncee.message.Receiver;
import top.imlk.ncee.query.Student;

import java.io.File;
import java.io.IOException;

public class ExcelWriter extends LogableRunnable implements Receiver {

    private Workbook resultWB;

    private Sheet luquSheet;
    private Sheet zongfenSheet;
    private Sheet jsonSheet;

    private StopAbleBlockingQueue<Student> writeOutStudentQueue;

    private String outFilePath;

    public ExcelWriter(StopAbleBlockingQueue<Student> writeOutStudentQueue, String outFilePath) {
        this.writeOutStudentQueue = writeOutStudentQueue;
        this.outFilePath = outFilePath;

        initTables();
    }

    @Override
    public void doRun() {
        this.writeOutStudentQueue.registerReceiver(this);

        int count = 0;
        while (true) {

            try {

                Student student;

                if ((student = determineReceive(writeOutStudentQueue, 7000)) == null) {
                    break;
                }

                writeStudent(student);
                count++;

                if (count % 10 == 0) {// 每十次保存一次
                    try {
                        resultWB.write(FileUtils.openOutputStream(new File(outFilePath)));
                    } catch (IOException e) {
                        logger.error("中途写入结果文件失败", e);
                    }

                }
            } catch (InterruptedException e) {
                break;
            }
        }


        this.writeOutStudentQueue.unregisterReceiver(this);
        try {

            resultWB.write(FileUtils.openOutputStream(new File(outFilePath)));


        } catch (IOException e) {
            logger.error("悲剧了，写入结果文件失败", e);
        } finally {
            try {
                if (resultWB != null) {
                    resultWB.close();
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

    }

    public void initTables() {

        resultWB = new HSSFWorkbook();

        zongfenSheet = resultWB.createSheet("总分");
        luquSheet = resultWB.createSheet("录取结果");
        jsonSheet = resultWB.createSheet("Json数据");
//        Sheet ptywSheet = resultWB.createSheet("普通语文");
//        Sheet ptlsSheet = resultWB.createSheet("普通理数");
//        Sheet ptwsSheet = resultWB.createSheet("普通文数");
//        Sheet ptwySheet = resultWB.createSheet("普通外语");
//        Sheet ptlzSheet = resultWB.createSheet("普通理综");
//        Sheet ptwzSheet = resultWB.createSheet("普通文综");
//        Sheet sxywSheet = resultWB.createSheet("sxyw");
//        Sheet sxsxSheet = resultWB.createSheet("sxsx");
//        Sheet sxwySheet = resultWB.createSheet("sxyw");
//        Sheet sxjsjSheet = resultWB.createSheet("sxjsj");
//        Sheet ptjsSheet = resultWB.createSheet("普通技术");


        initZongFenTableTitle();
        initLuquTableTitle();
        initJsonTitle();


    }

    public void writeStudent(Student student) {

        try {
            writeLuquTable(student);
        } catch (Throwable t) {
            logger.error("写入录取表时发生异常 Student：" + student, t);
        }


        try {
            writeZongFenTable(student);
        } catch (Throwable t) {
            logger.error("写入总分表时发生异常 Student：" + student, t);
        }


        try {
            writeJsonTable(student);
        } catch (Throwable t) {
            logger.error("写入JSON表时发生异常 Student：" + student, t);
        }

    }

    private void writeJsonTable(Student student) {
        Row row = jsonSheet.createRow(student.sourceRowNum);

        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.JsonTable.jsonColumnMap, "xm", student.name);
        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.JsonTable.jsonColumnMap, "key1", student.ksh);
        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.JsonTable.jsonColumnMap, "key2", student.sfzh);

        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.JsonTable.jsonColumnMap, "query_body", student.query_result_body);

        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.JsonTable.jsonColumnMap, "zongfen", student._score_str);
        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.JsonTable.jsonColumnMap, "xiaofen", student._scores_str);
        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.JsonTable.jsonColumnMap, "luqu", student._luqu_str);

    }

    private void writeZongFenTable(Student student) {
        Row row = zongfenSheet.createRow(student.sourceRowNum);

        if (student._score_json != null) {

            for (String key : student._score_json.keySet()) {
                ResultTable.insertStringIntoColumnIfDefined(
                        row,
                        ResultTable.ZongFenTable.zongfenColumnMap,
                        key,
                        String.valueOf(student._score_json.getString(key)).trim());
            }
        } else {
            ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.ZongFenTable.zongfenColumnMap, "xm", student.name);
            ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.ZongFenTable.zongfenColumnMap, "ksh", student.ksh);
            ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.ZongFenTable.zongfenColumnMap, "sfzh4w", student.sfzh);
        }

    }


    private void writeLuquTable(Student student) {
        Row row = luquSheet.createRow(student.sourceRowNum);

        if (student._luqu_json != null) {
            for (String key : student._luqu_json.keySet()) {
                ResultTable.insertStringIntoColumnIfDefined(
                        row,
                        ResultTable.LuquTable.luquColumnMap,
                        key,
                        String.valueOf(student._luqu_json.getString(key)).trim());
            }
        } else {
            ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.LuquTable.luquColumnMap, "xm", student.name);
            ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.LuquTable.luquColumnMap, "ksh", student.ksh);
            ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.LuquTable.luquColumnMap, "sfzh", student.sfzh);
        }
    }

    private void initJsonTitle() {
        Row row = jsonSheet.createRow(0);
        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.JsonTable.jsonColumnMap, "xm", "姓名");
        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.JsonTable.jsonColumnMap, "key1", "key1");
        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.JsonTable.jsonColumnMap, "key2", "key2");

        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.JsonTable.jsonColumnMap, "query_body", "query_body");
        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.JsonTable.jsonColumnMap, "zongfen", "_score");
        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.JsonTable.jsonColumnMap, "xiaofen", "_scores");
        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.JsonTable.jsonColumnMap, "luqu", "_luqu");

    }

    private void initZongFenTableTitle() {
        Row row = zongfenSheet.createRow(0);
        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.ZongFenTable.zongfenColumnMap, "xm", "姓名");
        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.ZongFenTable.zongfenColumnMap, "ksh", "考生号");
        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.ZongFenTable.zongfenColumnMap, "sfzh4w", "身份证号");
        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.ZongFenTable.zongfenColumnMap, "zkzh", "准考证号");

        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.ZongFenTable.zongfenColumnMap, "yw", "语文");
        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.ZongFenTable.zongfenColumnMap, "sx", "数学");
        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.ZongFenTable.zongfenColumnMap, "wy", "外语");
        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.ZongFenTable.zongfenColumnMap, "zh", "综合");
        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.ZongFenTable.zongfenColumnMap, "js", "技术");
//        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.ZongFenTable.zongfenColumnMap, "rw", "日文");
        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.ZongFenTable.zongfenColumnMap, "jf", "加分");

        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.ZongFenTable.zongfenColumnMap, "bkpmf", "本科总分（含加分）");
        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.ZongFenTable.zongfenColumnMap, "bkpm", "本科排名");
        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.ZongFenTable.zongfenColumnMap, "zkpmf", "专科总分（含加分）");
        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.ZongFenTable.zongfenColumnMap, "zkpm", "专科总分");
    }


    private void initLuquTableTitle() {
        Row row = luquSheet.createRow(0);

        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.LuquTable.luquColumnMap, "xm", "姓名");
        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.LuquTable.luquColumnMap, "ksh", "考生号");
        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.LuquTable.luquColumnMap, "sfzh", "身份号");
        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.LuquTable.luquColumnMap, "zkzh", "准考证号");
        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.LuquTable.luquColumnMap, "yxmc", "院校名称");
        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.LuquTable.luquColumnMap, "zymc", "专业名称");
        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.LuquTable.luquColumnMap, "pcmc", "批次名称");
        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.LuquTable.luquColumnMap, "klmc", "科类名称");
        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.LuquTable.luquColumnMap, "jhmc", "考试方式");
        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.LuquTable.luquColumnMap, "lqsj", "录取时间");
        ResultTable.insertStringIntoColumnIfDefined(row, ResultTable.LuquTable.luquColumnMap, "yxdh", "录取状态");
    }


    @Override
    public boolean needMoreData() {
        return true;
    }
}
