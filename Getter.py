# coding:utf-8

'''
Created on 2017年9月15日

@author: imlk
'''

import threading
import urllib
import urllib2
from bs4 import BeautifulSoup
import re
import time
import random
import json


class Getter(threading.Thread):
    
    def __init__(self, getterID,logUtil):
        threading.Thread.__init__(self)
        
        self.getterID = getterID
        self.logUtil = logUtil
        
        self.flag = 0
        self.resultCode = 0
        self.exit = 0
        # self.values = {}
        # self.values['dmlx'] = "1"
        # self.values['va'] = "UKywzivX"
        # self.values['year'] = "1736"
        # self.values['ct'] = None  # 模式 考生号or准考证号码
        # self.values['code'] = None
        # self.values['sfzh'] = None
        # self.values['yzm'] = "000000"

        self.student = None

        self.studentResolved = False
    
    def setStudent(self, student):
        self.student = student
        
    def getStudent(self):
        return self.student

    def hasResolvedStudent(self):
        return self.studentResolved

    
    def run(self):
        threading.Thread.run(self)
        
        while True:
            
            if self.flag == 1:
                
                self.resultCode = 0
                self.studentResolved = False
                
                # self.initNetValue()
                self.student.tryTime += 1

                # data = urllib.urlencode(self.values)
                # url = "http://gkcf.jxedu.gov.cn/cjcx/LqQuerySelvet"
                # url = "http://gkcf.jxedu.gov.cn/cjcx/CjQuerySelvet"

                # url = "http://59.63.178.44:81/ncee/temptotal?rnd={0}&StudentNo={1}&SFZH4W={2}".format(random.random(), self.student.studentID,self.student.studentSFZH[14:18])

                url = "http://59.63.178.44:90/ncee/temptotal?rnd={0}&StudentNo={1}&SFZH4W={2}".format(random.random(), self.student.studentID,self.student.studentSFZH[14:18])
                
                # url = "http://www.runoob.com/python/python-json.html"

                req = urllib2.Request(url, data = "")

                resp = None
                html_doc = None

                try:
                    resp = urllib2.urlopen(req,timeout=10)
                    
                    if resp.getcode() == 200:

                        # html_doc = resp.read().decode('gbk').encode('utf-8')
                        html_doc = resp.read()
                        
                        # html_doc = '{"success":1,"score":{"ksh":"18360731150001","zkzh":"273103124","xm":"陈文龙                                                          ","sfzH4W":"4351","yw":"117","sx":"140","wy":"132","zh":"249","js":"0","rw":"0","jf":"0","wj":"0","bkpmf":"638","bkpm":"2262","zkpmf":"389","zkpm":"19548","mstbzhcj":0.0,"xwtbzhcj":0.0,"bztbzhcj":0.0,"mstbpm":0,"ms2bpm":0,"ms3bpm":0,"mszkpm":0,"yyxtbpm":0,"yyx2bpm":0,"yyx3bpm":0,"yyxzkpm":0,"wdtbpm":0,"wd2bpm":0,"wd3bpm":0,"wdzkpm":0,"tywdtbpm":0,"tywd2bpm":0,"tywd3bpm":0,"tywdzkpm":0,"jmctbpm":0,"jmc2bpm":0,"jmc3bpm":0,"jmczkpm":0,"xwtbpm":0,"xw2bpm":0,"xw3bpm":0,"xwzkpm":0,"bztbpm":0,"bz2bpm":0,"bz3bpm":0,"bzzkpm":0,"ty2bpm":0,"tyzkpm":0}}'

                        # print html_doc
                        
                        hjson = json.loads(html_doc)

                        if hjson == [] or hjson == {} or hjson == None or hjson == "" or hjson["success"] != 1:
                            self.student.flag = 1  # 无信息

                            print html_doc                        
                            
                            self.logUtil.mprint(1, u"[第{3}次尝试] {0}\t{1} {2}\t无信息".format(self.student.studentName, self.student.studentID, self.student.studentSFZH,self.student.tryTime))
                        else:
                            self.resolveStudentInf(hjson)
                            self.studentResolved = True
                            if self.student.tryTime != 1:

                                print html_doc

                                self.logUtil.mprint(1, u"[第{3}次尝试] {0}\t{1} {2}\t成功".format(self.student.studentName, self.student.studentID, self.student.studentSFZH,self.student.tryTime))


                    else:
                        
                        print u"[第{3}次尝试] {0}\t{1} {2}\t连接失败(返回码{4})".format(self.student.studentName, self.student.studentID, self.student.studentSFZH,self.student.tryTime,resp.getcode())
                        self.resultCode = -1  
                        
                except BaseException, e:
                    print html_doc
                    self.logUtil.mprint(1, u"[第{3}次尝试] {0}\t{1} {2}\t连接失败 {4}".format(self.student.studentName, self.student.studentID, self.student.studentSFZH,self.student.tryTime,e))
                    self.resultCode = -1
                finally:
                    if resp:
                        resp.close()
                    

                if self.studentResolved or self.student.tryTime >= 15:
                    self.flag = 2  # 完成一项任务
                else:
                    time.sleep(0.7)
                
            if self.exit == 1 and (self.flag == 2 or self.flag == 0):
                break
                
                
    # def initNetValue(self):
                        
    #     values = self.values
    #     if len(self.student.studentID) == 14:
    #         values['ct'] = "1"
    #         values['code'] = self.student.studentID[4:14]

    #     elif len(self.student.studentID) == 9:
    #         values['ct'] = "2"
    #         values['code'] = self.student.studentID
            
    #     if len(self.student.studentSFZH) == 4:
    #         values['sfzh'] = self.student.studentSFZH
    #     elif len(self.student.studentSFZH) == 18:
    #         values['sfzh'] = self.student.studentSFZH[14:18]
                

    def resolveStudentInf(self, hjson):
        
        self.student.ksh = hjson["score"]["ksh"]
        self.student.zkzh = hjson["score"]["zkzh"]
        self.student.bkzf = hjson["score"]["bkpmf"]
        self.student.bkpm = hjson["score"]["bkpm"]
        self.student.zkzf = hjson["score"]["zkpmf"]
        self.student.zkpm = hjson["score"]["zkpm"]

        self.student.jf = hjson["score"]["jf"]
        self.student.yw = hjson["score"]["yw"]
        self.student.sx = hjson["score"]["sx"]
        self.student.yy = hjson["score"]["wy"]
        self.student.zh = hjson["score"]["zh"]
        self.student.js = hjson["score"]["js"]

        # if (firstN == "0") {

        #     // 三校生
        #     $yw.eq(0).text("三校语文成绩");
        #     $sx.eq(0).text("三校数学成绩");
        #     $wy.eq(0).text("三校外语成绩");
        #     $zh.eq(0).text("三校计算机成绩");
        #     $(".js").hide(); //$js.eq(0).text("三校技术成绩");
        #     //$rw.eq(0).text("人武成绩");
        #     //$jf.eq(0).text("优惠加分");
        #     //$wj.eq(0).text("违规情况");
        #     $bkpmf.eq(0).text("三校总分(含加分)");
        #     $bkpm.eq(0).text("三校平行排名");


        # } else {
        #     // 正常
        #     $yw.eq(0).text("语文成绩");
        #     $sx.eq(0).text("数学成绩");
        #     $wy.eq(0).text("外语成绩");
        #     $zh.eq(0).text("综合成绩");
        #     $js.eq(0).text("技术成绩");
        #     //$rw.eq(0).text("人武成绩");
        #     //$jf.eq(0).text("优惠加分");
        #     //$wj.eq(0).text("违规情况");
        #     $bkpmf.eq(0).text("本科总分(含加分)");
        #     $bkpm.eq(0).text("本科分平行排名");
        #     $(".zkpmf").show();
        #     $(".zkpm").show();
        # }


        # $yw.eq(1).text(score.yw);
        # $sx.eq(1).text(score.sx);
        # $wy.eq(1).text(score.wy);
        # $zh.eq(1).text(score.zh);
        # $js.eq(1).text(score.js);

        # $bkpmf.eq(1).text(score.bkpmf);
        # $bkpm.eq(1).text(score.bkpm);
        # $zkpmf.eq(1).text(score.zkpmf);
        # $zkpm.eq(1).text(score.zkpm);

        # if (score.rw > 0) {
        #     $(".rw").show();
        #     $rw.eq(1).text(score.rw);
        # }
        # if (score.jf > 0) {
        #     $(".jf").show();
        #     $jf.eq(1).text(score.jf);
        # }
        # if (score.wj > 0) {
        #     $(".wj").show();
        # }



        # count = 0

        # for one in ones:
        #     print "@@@@@" + str(count) + "@@@@@\n" + one.get_text()
        #     count = count + 1

        # if u'考生姓名' in ones[4].get_text():
        #     start = 15
        #     self.student.ksh = re.findall("\d+", ones[start].get_text())[0]
        #     start += 1
        #     self.student.zkzh = re.findall("\d+", ones[start].get_text())[0]
        #     start += 1
        #     self.student.bkzf = re.findall("\d+", ones[start].get_text())[0]
        #     start += 1
        #     self.student.bkpm = re.findall("\d+", ones[start].get_text())[0]
        #     start += 1
        #     self.student.zkzf = re.findall("\d+", ones[start].get_text())[0]
        #     start += 1
        #     self.student.zkpm = re.findall("\d+", ones[start].get_text())[0]
        #     start += 1

        #     # self.student.ksh = re.findall("\d+", ones[15].get_text())[0]
        #     # self.student.zkzh = re.findall("\d+", ones[16].get_text())[0]
        #     # self.student.bkzf = re.findall("\d+", ones[17].get_text())[0]
        #     # self.student.bkpm = re.findall("\d+", ones[18].get_text())[0]
        #     # self.student.zkzf = re.findall("\d+", ones[19].get_text())[0]
        #     # self.student.zkpm = re.findall("\d+", ones[20].get_text())[0]
                
        #     if u'加 分' in ones[4].get_text():
        #         # start = 15
        #         self.student.yw = re.findall("\d+", ones[28].get_text())[0]
        #         self.student.sx = re.findall("\d+", ones[29].get_text())[0]
        #         self.student.yy = re.findall("\d+", ones[30].get_text())[0]
        #         self.student.zh = re.findall("\d+", ones[31].get_text())[0]
        #         self.student.js = re.findall("\d+", ones[32].get_text())[0]
                
        #         self.student.jf = re.findall("\d+", ones[33].get_text())[0]

        #         # self.student.yw = re.findall("\d+", ones[28].get_text())[0]
        #         # self.student.sx = re.findall("\d+", ones[29].get_text())[0]
        #         # self.student.yy = re.findall("\d+", ones[30].get_text())[0]
        #         # self.student.zh = re.findall("\d+", ones[31].get_text())[0]
        #         # self.student.js = re.findall("\d+", ones[32].get_text())[0]
                
        #         # self.student.jf = re.findall("\d+", ones[33].get_text())[0]

        #     else:
        #         self.student.jf = '0'
                
        #         self.student.yw = re.findall("\d+", ones[27].get_text())[0]
        #         self.student.sx = re.findall("\d+", ones[28].get_text())[0]
        #         self.student.yy = re.findall("\d+", ones[29].get_text())[0]
        #         self.student.zh = re.findall("\d+", ones[30].get_text())[0]
        #         self.student.js = re.findall("\d+", ones[31].get_text())[0]


        #     if u'录取状态' in ones[4].get_text():
        #         self.student.flag = 3
        #         s = ''.join(ones[4].get_text().split())
        #         # print s
        #         s = s.split(u'录取状态：')[1]
        #         s = s.split(u'考生号：') 
        #         self.student.lqzt = s[0]
        #         s = (s[1].split(u'计划性质名称：')[1]).split(u'录取专业：')
        #         self.student.jhxzmc = s[0]
        #         s = s[1].split(u'录取批次：')
        #         self.student.lqzy = s[0]
        #         s = s[1].split(u'录取科类：')
        #         self.student.lqpc = s[0]
        #         s = s[1].split(u'录取时间：')
        #         self.student.lqkl = s[0]
        #         s = s[1].split(u'院校代号(省标)：')
        #         self.student.lqsj = s[0]
        #         s = s[1].split(u'录取院校：')
        #         self.student.yxdh = s[0]
        #         s = s[1].split(u'退出')
        #         self.student.lqyx = s[0]
                
        #     else:
        #         self.student.flag = 2
        
