#coding:utf-8

'''
Created on 2017年9月15日

@author: imlk
'''
import threading
import xlwt
import time
from LogUtil import LogUtil

class Writter(threading.Thread):
    
    def __init__(self,studentNum,logUtil):
        threading.Thread.__init__(self)
        
        self.studentNum = studentNum
        self.logUtil = logUtil
        self.writtenStudentNum = 0
        
        
        self.flag = 1#程序进行中
        
        self.studentList = []
        
        self.aim_wb = xlwt.Workbook()
    
        self.aim_sh = self.aim_wb.add_sheet("Sheet1")
        start = 0
        self.aim_sh.write(0, start,u'学生序号')
        start += 1
        self.aim_sh.write(0, start,u'姓名')
        start += 1

        self.aim_sh.write(0, start,u'考生号/准考证号')
        start += 1
        self.aim_sh.write(0, start,u'身份证号码')
        start += 1

        self.aim_sh.write(0, start,u'考生号')
        start += 1
        self.aim_sh.write(0, start,u'准考证号')
        start += 1

        self.aim_sh.write(0, start,u'本科总分(含加分)')
        start += 1
        self.aim_sh.write(0, start,u'本科排名')
        start += 1
        self.aim_sh.write(0, start,u'专科总分(含加分)')
        start += 1
        self.aim_sh.write(0, start,u'专科排名')
        start += 1
        self.aim_sh.write(0, start,u'语文')
        start += 1
        self.aim_sh.write(0, start,u'数学')
        start += 1
        self.aim_sh.write(0, start,u'外语')
        start += 1
        self.aim_sh.write(0, start,u'综合')
        start += 1
        self.aim_sh.write(0, start,u'技术')
        start += 1
        self.aim_sh.write(0, start,u'加分')
        start += 1
    
        self.aim_sh.write(0, start,u'录取状态')
        start += 1
        self.aim_sh.write(0, start,u'计划性质名称')
        start += 1
        self.aim_sh.write(0, start,u'录取专业')
        start += 1
        self.aim_sh.write(0, start,u'录取批次')
        start += 1
        self.aim_sh.write(0, start,u'录取科类')
        start += 1
        self.aim_sh.write(0, start,u'录取时间')
        start += 1
        self.aim_sh.write(0, start,u'院校代号(省标)')
        start += 1
        self.aim_sh.write(0, start,u'录取院校')
        start += 1
        
        self.error_wb = xlwt.Workbook()
        self.error_sh = self.error_wb.add_sheet("Sheet1")
        start = 0
        self.error_sh.write(0, start,u'学生序号')
        start += 1
        self.error_sh.write(0, start,u'姓名')
        start += 1
        self.error_sh.write(0, start,u'考生号/准考证号')
        start += 1
        self.error_sh.write(0, start,u'身份证号码')
        start += 1
        
        self.errorStudentNum = 0
        

        nowTime = int(time.time())
        self.aim_path = "aim{0}.xls".format(nowTime)
        self.error_path = "error{0}.xls".format(nowTime)
        


    def addStudent(self,student):
        self.studentList.append(student)
        
#         print "add",student.studentName
        
    
    def writeStudent(self,student):
        
        if student.flag == -1:
            self.errorStudentNum = self.errorStudentNum + 1
            start = 0
            self.error_sh.write(self.errorStudentNum,start,student.studentNO)
            start += 1
            self.error_sh.write(self.errorStudentNum,start,student.studentName)
            start += 1
            self.error_sh.write(self.errorStudentNum,start,student.studentID)
            start += 1
            self.error_sh.write(self.errorStudentNum,start,student.studentSFZH)
            start += 1
            self.error_sh.write(self.errorStudentNum,start,u'连接失败')
            start += 1
            
            start = 0
            self.aim_sh.write(student.studentNO,start,student.studentNO)
            start += 1
            self.aim_sh.write(student.studentNO,start,student.studentName)
            start += 1
            self.aim_sh.write(student.studentNO,start,student.studentID)
            start += 1
            self.aim_sh.write(student.studentNO,start,student.studentSFZH)

            start += 3
            self.aim_sh.write(student.studentNO,start,u'连接失败')
            
        elif student.flag == 1:
            self.errorStudentNum = self.errorStudentNum + 1
            
            start = 0
            self.error_sh.write(self.errorStudentNum,start,student.studentNO)
            start += 1
            self.error_sh.write(self.errorStudentNum,start,student.studentName)
            start += 1
            self.error_sh.write(self.errorStudentNum,start,student.studentID)
            start += 1
            self.error_sh.write(self.errorStudentNum,start,student.studentSFZH)
            start += 1
            self.error_sh.write(self.errorStudentNum,start,u'无信息')
            start += 1
            
            start = 0
            self.aim_sh.write(student.studentNO,start,student.studentNO)
            start += 1
            self.aim_sh.write(student.studentNO,start,student.studentName)
            start += 1
            self.aim_sh.write(student.studentNO,start,student.studentID)
            start += 1
            self.aim_sh.write(student.studentNO,start,student.studentSFZH)
            start += 3
            self.aim_sh.write(student.studentNO,start,u'无信息')
            start += 1
            
        else:
            start = 0
            self.aim_sh.write(student.studentNO,start,student.studentNO)
            start += 1
            self.aim_sh.write(student.studentNO,start,student.studentName)
            start += 1
            self.aim_sh.write(student.studentNO,start,student.studentID)
            start += 1
            self.aim_sh.write(student.studentNO,start,student.studentSFZH)
            start += 1
            self.aim_sh.write(student.studentNO,start,student.ksh)
            start += 1
            self.aim_sh.write(student.studentNO,start,student.zkzh)
            start += 1
            self.aim_sh.write(student.studentNO,start,student.bkzf)
            start += 1
            self.aim_sh.write(student.studentNO,start,student.bkpm)
            start += 1
            self.aim_sh.write(student.studentNO,start,student.zkzf)
            start += 1
            self.aim_sh.write(student.studentNO,start,student.zkpm)
            start += 1
            self.aim_sh.write(student.studentNO,start,student.yw)
            start += 1
            self.aim_sh.write(student.studentNO,start,student.sx)
            start += 1
            self.aim_sh.write(student.studentNO,start,student.yy)
            start += 1
            self.aim_sh.write(student.studentNO,start,student.zh)
            start += 1
            self.aim_sh.write(student.studentNO,start,student.js)
            start += 1
            self.aim_sh.write(student.studentNO,start,student.jf)
            start += 1

            
            if student.flag == 2:
                self.aim_sh.write(student.studentNO,16,u'未查询到录取信息')
            elif student.flag == 3:
                start = 17
                self.aim_sh.write(student.studentNO,start,student.lqzt)
                start += 1
                self.aim_sh.write(student.studentNO,start,student.jhxzmc)
                start += 1
                self.aim_sh.write(student.studentNO,start,student.lqzy)
                start += 1
                self.aim_sh.write(student.studentNO,start,student.lqpc)
                start += 1
                self.aim_sh.write(student.studentNO,start,student.lqkl)
                start += 1
                self.aim_sh.write(student.studentNO,start,student.lqsj)
                start += 1
                self.aim_sh.write(student.studentNO,start,student.yxdh)
                start += 1
                self.aim_sh.write(student.studentNO,start,student.lqyx)
                start += 1
        
        
        self.writtenStudentNum = self.writtenStudentNum + 1
        self.logUtil.mprint(0,'[' + '#'* (self.writtenStudentNum*50/self.studentNum) + ' ' * (50 - (self.writtenStudentNum*50/self.studentNum)) + ']' + str(self.writtenStudentNum) + '/' + str(self.studentNum)) 
    
    def run(self):
        while self.flag == 1:
            if self.studentList != []:
                student = self.studentList[0]
                self.writeStudent(student)
                self.studentList.remove(student)
                self.aim_wb.save(self.aim_path)
                self.error_wb.save(self.error_path)
                
        if self.flag == 0 and self.studentList != []:
            for student in self.studentList:
                self.writeStudent(student)
                self.aim_wb.save(self.aim_path)
                self.error_wb.save(self.error_path)
                
        
        
        self.aim_wb.save(self.aim_path)
        self.error_wb.save(self.error_path)