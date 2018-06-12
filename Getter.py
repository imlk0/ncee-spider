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


class Getter(threading.Thread):
    
    def __init__(self, getterID,logUtil):
        threading.Thread.__init__(self)
        
        self.getterID = getterID
        self.logUtil = logUtil
        
        self.flag = 0
        self.resultCode = 0
        self.exit = 0
        self.values = {}
        self.values['dmlx'] = "1"
        self.values['va'] = "UKywzivX"
        self.values['year'] = "1736"
        self.values['ct'] = None  # 模式 考生号or准考证号码
        self.values['code'] = None
        self.values['sfzh'] = None
        self.values['yzm'] = "000000"

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
                
                self.initNetValue()
                self.student.tryTime += 1

                data = urllib.urlencode(self.values)
                url = "http://gkcf.jxedu.gov.cn/cjcx/LqQuerySelvet"
                # url = "http://gkcf.jxedu.gov.cn/cjcx/CjQuerySelvet"
                
                req = urllib2.Request(url, data)

                resp = None

                try:
                    resp = urllib2.urlopen(req,timeout=10)
                    
                    if resp.getcode() == 200:
                        
                        html_doc = resp.read().decode('gbk').encode('utf-8')
                        # print html_doc
                        soup = BeautifulSoup(html_doc, 'html.parser', from_encoding='utf-8')
                        
                        ones = soup.find_all('td')
                        
                        if ones == []:
                            self.student.flag = 1  # 无信息
                            self.logUtil.mprint(1, u"[第{3}次尝试] {0} {1} {2} 无信息".format(self.student.studentName, self.student.studentID, self.student.studentSFZH,self.student.tryTime))
                        else:
                            self.resolveStudentInf(ones)
                            self.studentResolved = True
                            if self.student.tryTime != 1:
                                self.logUtil.mprint(1, u"[第{3}次尝试] {0} {1} {2} 成功".format(self.student.studentName, self.student.studentID, self.student.studentSFZH,self.student.tryTime))


                    else:
                        print u"[第{3}次尝试] {0} {1} {2}连接失败(返回码{4})".format(self.student.studentName, self.student.studentID, self.student.studentSFZH,self.student.tryTime,resp.getcode())
                        self.resultCode = -1  
                        
                except IOError:
                    self.logUtil.mprint(1, u"[第{3}次尝试] {0} {1} {2} 连接被服务器阻断".format(self.student.studentName, self.student.studentID, self.student.studentSFZH,self.student.tryTime))
                    self.resultCode = -1
                except urllib2.URLError:
                    self.logUtil.mprint(1, u"[第{3}次尝试]{0} {1} {2} 连接失败".format(self.student.studentName, self.student.studentID, self.student.studentSFZH,self.student.tryTime))
                    self.resultCode = -1
                finally:
                    if resp:
                        resp.close()
                    

                if self.studentResolved or self.student.tryTime >= 5:
                    self.flag = 2  # 完成一项任务
                
            if self.exit == 1 and (self.flag == 2 or self.flag == 0):
                break
                
                
    def initNetValue(self):
                        
        values = self.values
        if len(self.student.studentID) == 14:
            values['ct'] = "1"
            values['code'] = self.student.studentID[4:14]

        elif len(self.student.studentID) == 9:
            values['ct'] = "2"
            values['code'] = self.student.studentID
            
        if len(self.student.studentSFZH) == 4:
            values['sfzh'] = self.student.studentSFZH
        elif len(self.student.studentSFZH) == 18:
            values['sfzh'] = self.student.studentSFZH[14:18]
                

    def resolveStudentInf(self, ones):
        
        # count = 0

        # for one in ones:
        #     print "@@@@@" + str(count) + "@@@@@\n" + one.get_text()
        #     count = count + 1

        if u'考生姓名' in ones[4].get_text():
            
            self.student.ksh = re.findall("\d+", ones[15].get_text())[0]
            self.student.zkzh = re.findall("\d+", ones[16].get_text())[0]

            self.student.bkzf = re.findall("\d+", ones[17].get_text())[0]
            self.student.bkpm = re.findall("\d+", ones[18].get_text())[0]
            self.student.zkzf = re.findall("\d+", ones[19].get_text())[0]
            self.student.zkpm = re.findall("\d+", ones[20].get_text())[0]
                
            if u'加 分' in ones[4].get_text():
                self.student.jf = re.findall("\d+", ones[33].get_text())[0]
                
                self.student.yw = re.findall("\d+", ones[28].get_text())[0]
                self.student.sx = re.findall("\d+", ones[29].get_text())[0]
                self.student.yy = re.findall("\d+", ones[30].get_text())[0]
                self.student.zh = re.findall("\d+", ones[31].get_text())[0]
                self.student.js = re.findall("\d+", ones[32].get_text())[0]
                
            else:
                self.student.jf = '0'
                
                self.student.yw = re.findall("\d+", ones[27].get_text())[0]
                self.student.sx = re.findall("\d+", ones[28].get_text())[0]
                self.student.yy = re.findall("\d+", ones[29].get_text())[0]
                self.student.zh = re.findall("\d+", ones[30].get_text())[0]
                self.student.js = re.findall("\d+", ones[31].get_text())[0]

            if u'录取状态' in ones[4].get_text():
                self.student.flag = 3
                s = ''.join(ones[4].get_text().split())
                # print s
                s = s.split(u'录取状态：')[1]
                s = s.split(u'考生号：') 
                self.student.lqzt = s[0]
                s = (s[1].split(u'计划性质名称：')[1]).split(u'录取专业：')
                self.student.jhxzmc = s[0]
                s = s[1].split(u'录取批次：')
                self.student.lqzy = s[0]
                s = s[1].split(u'录取科类：')
                self.student.lqpc = s[0]
                s = s[1].split(u'录取时间：')
                self.student.lqkl = s[0]
                s = s[1].split(u'院校代号(省标)：')
                self.student.lqsj = s[0]
                s = s[1].split(u'录取院校：')
                self.student.yxdh = s[0]
                s = s[1].split(u'退出')
                self.student.lqyx = s[0]
                
            else:
                self.student.flag = 2
        
