package top.imlk.ncee.input;

import org.apache.commons.io.FileUtils;
import org.apache.poi.hssf.usermodel.HSSFWorkbook;
import org.apache.poi.openxml4j.exceptions.InvalidFormatException;
import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import top.imlk.ncee.abstracts.LogableRunnable;
import top.imlk.ncee.abstracts.StopAbleBlockingQueue;
import top.imlk.ncee.message.Sender;
import top.imlk.ncee.query.Student;

import java.io.File;
import java.io.IOException;

public class ExcelReader extends LogableRunnable implements Sender {


    public ExcelReader(String fileName, StopAbleBlockingQueue<Student> blockingQueue) {
        this.fileName = fileName;
        this.blockingQueue = blockingQueue;
    }

    private String fileName;
    private StopAbleBlockingQueue<Student> blockingQueue;

    @Override
    public boolean willBeMoreData() {

        return true;
    }

    @Override
    public void doRun() {

        this.blockingQueue.registerSender(this);

        readAndArrangeStudent();

        this.blockingQueue.unregisterSender(this);

    }


    public void readAndArrangeStudent() {


        File file = new File(fileName);


        if (file.exists()) {

            Workbook studentsWB = null;

            try {

                if (file.getAbsolutePath().endsWith(".xls")) {

                    studentsWB = new HSSFWorkbook(FileUtils.openInputStream(file));

                } else if (file.getAbsolutePath().endsWith("xlsx")) {

                    studentsWB = new XSSFWorkbook(file);

                } else {
                    throw new InvalidFormatException("文件 " + file.getAbsolutePath() + " 不支持的格式");
                }


                Sheet sheet = studentsWB.getSheetAt(0);

                int nameColumnInd = 0;
                int kshColumnInd = 1;
                int sfzhColumnInd = 2;

                int firstRowNum = sheet.getFirstRowNum();
                int lastRowNum = sheet.getLastRowNum();

//                int startRowNum = firstRowNum + 1;

                int id = 0;

                for (int rowNum = firstRowNum; rowNum <= lastRowNum; ++rowNum) {
                    Row row = sheet.getRow(rowNum);
                    try {
                        String name = row.getCell(nameColumnInd).getStringCellValue();
                        Cell cell;
                        cell = row.getCell(kshColumnInd);
                        String ksh = cell.getCellType() == CellType.NUMERIC ? String.valueOf((long) cell.getNumericCellValue()) : cell.getStringCellValue();

                        String sfzh = row.getCell(sfzhColumnInd).getStringCellValue();

                        if (Student.isAStudent(name, ksh, sfzh)) {
                            id++;

                            Student student = new Student();
                            student.sourceRowNum = rowNum;
                            student.name = name;
                            student.ksh = ksh;
                            student.sfzh = sfzh;
                            student.id = id;


                            try {
                                blockingQueue.put(student);

                            } catch (InterruptedException e) {
                                logger.info("{} 遭遇中断", this);
                                break;
                            }

                        }

                    } catch (Throwable t) {
                        logger.error("读取第{}行的单元格失败,已跳过", rowNum);
                    }
                }


            } catch (IOException e) {
                logger.error("IO异常", e);
            } catch (InvalidFormatException e) {
                logger.error("不支持的输入文件格式", e);
            } catch (Throwable e) {
                logger.error("未知异常", e);
            } finally {

                try {
                    if (studentsWB != null) {
                        studentsWB.close();
                    }
                } catch (IOException ioe) {
                    logger.error("Workbook 关闭失败", ioe);
                }
            }
        } else {
            logger.error("文件 {} 不存在", file.getAbsolutePath());
        }


    }


}
