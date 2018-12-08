package top.imlk.ncee.query;

import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import org.apache.commons.codec.binary.StringUtils;

public class Student {

    public int id;

    public String name;

    public String ksh;

    public String sfzh;

    public String token;


    public int sourceRowNum;


    public Student(String name, String ksh, String sfzh, String token) {
        this.name = name;
        this.ksh = ksh;
        this.sfzh = sfzh;
        this.token = token;
    }

    @Override
    public String toString() {
        return "Student{" +
                "name='" + name + '\'' +
                ", ksh='" + ksh + '\'' +
                ", sfzh='" + sfzh + '\'' +
                ", token='" + token + '\'' +
                ", sourceRowNum=" + sourceRowNum +
                ", _score_str='" + _score_str + '\'' +
                ", _scores_str='" + _scores_str + '\'' +
                ", _luqu_str='" + _luqu_str + '\'' +
//                ", query_result_body='" + query_result_body + '\'' +
                '}';
    }

    public JSONObject _score_json;
    public JSONArray _scores_json;
    public JSONObject _luqu_json;

    public String _score_str;
    public String _scores_str;
    public String _luqu_str;


    public String query_result_body;
    public int failedCount;


    public Student() {

    }


    public static boolean isAStudent(String name, String ksh, String sfzh) {
        if (ksh == null || "".equals(ksh.trim()) || sfzh == null || "".equals(sfzh.trim()) || !ksh.trim().matches("^[0-9]+$") || !sfzh.trim().matches("^[0-9]+[0-9xX]?$")) {
            return false;
        }

        return true;
    }
}
