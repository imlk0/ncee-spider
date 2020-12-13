# 🕷️ncee-spider

江西地区高考批量查分/查录取工具


## Usage

```
usage: main.py [-h] [-f SRC_FILE] [-o OUTPUT_FILE] [-t OUTPUT_CONTENT_TYPE] [-s QUERY_ORDER] [-c CONFIG_FILE] {i,e,s,f}

Program to get NCEE score.

positional arguments:
  {i,e,s,f}             sub_command. 
                        i: import student info
                        e: export score data
                        s: print statistic info
                        f: fetch student score from website

optional arguments:
  -h, --help            show this help message and exit
  -f SRC_FILE           student info from excel file
  -o OUTPUT_FILE        output excel file
  -t OUTPUT_CONTENT_TYPE
                        output content type. 0: 总分，1: 小分，2：录取. default: 0
  -s QUERY_ORDER        order to query student. 0: 随机，1: 顺序，2：倒序. default: 0
  -c CONFIG_FILE        config file path, default is ./configuration.yaml
```

**notice：**

1. 使用baidu-ocr服务识别验证码，请在手动注册申请，并在`configuration.yaml`中填入配置信息，

2. 该工具使用mongodb作为存储后端，使用默认mongodb配置，数据库名为`ncee_spider`，自定义需求请修改`db.py`文件


使用流程：

1. `python ./main.py i` 导入学生数据

2. `python ./main.py f` 爬取考生成绩、录取信息存储到数据库

3. `python ./main.py e` 按需求导出特定数据

可以使用`python ./main.py s`实时查看统计信息

