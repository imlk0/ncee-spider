package top.imlk.ncee.output;

import jdk.internal.org.objectweb.asm.tree.analysis.Value;
import org.apache.poi.ss.usermodel.Row;

import java.util.HashMap;
import java.util.Map;

public class ResultTable {


    static class JsonTable {
        public static Map<String, Integer> jsonColumnMap = new HashMap<>();

        static {

            addJsonColumn("xm");
            addJsonColumn("key1");
            addJsonColumn("key2");


            addJsonColumn("query_body");
            addJsonColumn("zongfen");
            addJsonColumn("xiaofen");
            addJsonColumn("luqu");

        }

        private static int jsonColumnNum = 0;

        private static void addJsonColumn(String columnName) {

            if (columnName == null) {
                //表示空开一列
            } else {
                jsonColumnMap.put(columnName, jsonColumnNum);
            }

            jsonColumnNum++;
        }

    }


    static class ZongFenTable {
        public static Map<String, Integer> zongfenColumnMap = new HashMap<>();

        static {
            addZongfenColumn("xm");
            addZongfenColumn("ksh");
            addZongfenColumn("sfzh4w");
            addZongfenColumn("zkzh");

            addZongfenColumn("yw");
            addZongfenColumn("sx");
            addZongfenColumn("wy");
            addZongfenColumn("zh");
            addZongfenColumn("js");
//            addZongfenColumn("rw");// 日文
            addZongfenColumn("jf");// 加分

            addZongfenColumn("bkpmf");
            addZongfenColumn("bkpm");
            addZongfenColumn("zkpmf");
            addZongfenColumn("zkpm");


        }

        private static int zongfenColumnNum = 0;

        private static void addZongfenColumn(String columnName) {

            if (columnName == null) {
                //表示空开一列
            } else {
                zongfenColumnMap.put(columnName, zongfenColumnNum);
            }

            zongfenColumnNum++;
        }

    }


    static class LuquTable {
        public static Map<String, Integer> luquColumnMap = new HashMap<>();

        static {
            addLuquColumn("xm");
            addLuquColumn("ksh");
            addLuquColumn("sfzh");
            addLuquColumn("zkzh");

            addLuquColumn("yxmc");
            addLuquColumn("zymc");
            addLuquColumn("pcmc");
            addLuquColumn("klmc");
            addLuquColumn("jhmc");
            addLuquColumn("lqsj");
            addLuquColumn("yxdh");

        }

        private static int luquColumnNum = 0;

        private static void addLuquColumn(String columnName) {

            if (columnName == null) {
                //表示空开一列
            } else {
                luquColumnMap.put(columnName, luquColumnNum);
            }

            luquColumnNum++;
        }

    }


    public static void insertStringIntoColumnIfDefined(Row row, Map<String, Integer> map, String mapkey, String value) {
        Integer id;
        if ((id = map.get(mapkey)) != null) {
            row.createCell(id)
                    .setCellValue(value);
        }
    }

}
