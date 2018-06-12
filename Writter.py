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
        self.aim_sh.write(0, 0,u'学生序号')
        self.aim_sh.write(0, 1,u'姓名')
        self.aim_sh.write(0, 2,u'考生号')
        self.aim_sh.write(0, 3,u'准考证号')
        self.aim_sh.write(0, 4,u'本科总分(含加分)')
        self.aim_sh.write(0, 5,u'本科排名')
        self.aim_sh.write(0, 6,u'专科总分(含加分)')
        self.aim_sh.write(0, 7,u'专科排名')
        self.aim_sh.write(0, 8,u'语文')
        self.aim_sh.write(0, 9,u'数学')
        self.aim_sh.write(0, 10,u'外语')
        self.aim_sh.write(0, 11,u'综合')
        self.aim_sh.write(0, 12,u'技术')
        self.aim_sh.write(0, 13,u'加分')
    
        self.aim_sh.write(0, 15,u'录取状态')
        self.aim_sh.write(0, 16,u'计划性质名称')
        self.aim_sh.write(0, 17,u'录取专业')
        self.aim_sh.write(0, 18,u'录取批次')
        self.aim_sh.write(0, 19,u'录取科类')
        self.aim_sh.write(0, 20,u'录取时间')
        self.aim_sh.write(0, 21,u'院校代号(省标)')
        self.aim_sh.write(0, 22,u'录取院校')
        
        self.error_wb = xlwt.Workbook()
        self.error_sh = self.error_wb.add_sheet("Sheet1")
        self.error_sh.write(0, 0,u'学生序号')
        self.error_sh.write(0, 1,u'姓名')
        self.error_sh.write(0, 2,u'考生号/准考证号')
        self.error_sh.write(0, 3,u'身份证号码')
        
        self.errorStudentNum = 0
        
    def addStudent(self,student):
        self.studentList.append(student)
        
#         print "add",student.studentName
        
    
    def writeStudent(self,student):
        
        if student.flag == -1:
            self.errorStudentNum = self.errorStudentNum + 1
            
            self.error_sh.write(self.errorStudentNum,0,student.studentNO)
            self.error_sh.write(self.errorStudentNum,1,student.studentName)
            self.error_sh.write(self.errorStudentNum,2,student.studentID)
            self.error_sh.write(self.errorStudentNum,3,student.studentSFZH)
            self.error_sh.write(self.errorStudentNum,4,u'连接失败')
            
            self.aim_sh.write(student.studentNO,0,student.studentNO)
            self.aim_sh.write(student.studentNO,1,student.studentName)
            self.aim_sh.write(student.studentNO,2,student.studentID)
            self.aim_sh.write(student.studentNO,4,u'连接失败')
            
        elif student.flag == 1:
            self.errorStudentNum = self.errorStudentNum + 1
            
            self.error_sh.write(self.errorStudentNum,0,student.studentNO)
            self.error_sh.write(self.errorStudentNum,1,student.studentName)
            self.error_sh.write(self.errorStudentNum,2,student.studentID)
            self.error_sh.write(self.errorStudentNum,3,student.studentSFZH)
            self.error_sh.write(self.errorStudentNum,4,u'无信息')
            
            self.aim_sh.write(student.studentNO,0,student.studentNO)
            self.aim_sh.write(student.studentNO,1,student.studentName)
            self.aim_sh.write(student.studentNO,2,student.studentID)
            self.aim_sh.write(student.studentNO,4,u'无信息')
            
        else:
            self.aim_sh.write(student.studentNO,0,student.studentNO)
            self.aim_sh.write(student.studentNO,1,student.studentName)
            self.aim_sh.write(student.studentNO,2,student.ksh)
            self.aim_sh.write(student.studentNO,3,student.zkzh)
            self.aim_sh.write(student.studentNO,4,student.bkzf)
            self.aim_sh.write(student.studentNO,5,student.bkpm)
            self.aim_sh.write(student.studentNO,6,student.zkzf)
            self.aim_sh.write(student.studentNO,7,student.zkpm)
            self.aim_sh.write(student.studentNO,8,student.yw)
            self.aim_sh.write(student.studentNO,9,student.sx)
            self.aim_sh.write(student.studentNO,10,student.yy)
            self.aim_sh.write(student.studentNO,11,student.zh)
            self.aim_sh.write(student.studentNO,12,student.js)
            self.aim_sh.write(student.studentNO,13,student.jf)

            
            if student.flag == 2:
                self.aim_sh.write(student.studentNO,14,u'未查询到录取信息')
            elif student.flag == 3:
                self.aim_sh.write(student.studentNO,15,student.lqzt)
                self.aim_sh.write(student.studentNO,16,student.jhxzmc)
                self.aim_sh.write(student.studentNO,17,student.lqzy)
                self.aim_sh.write(student.studentNO,18,student.lqpc)
                self.aim_sh.write(student.studentNO,19,student.lqkl)
                self.aim_sh.write(student.studentNO,20,student.lqsj)
                self.aim_sh.write(student.studentNO,21,student.yxdh)
                self.aim_sh.write(student.studentNO,22,student.lqyx)
        
        
        self.writtenStudentNum = self.writtenStudentNum + 1
        self.logUtil.mprint(0,'[' + '#'* (self.writtenStudentNum*50/self.studentNum) + ' ' * (50 - (self.writtenStudentNum*50/self.studentNum)) + ']' + str(self.writtenStudentNum) + '/' + str(self.studentNum)) 
    
    def run(self):
        while self.flag == 1:
            if self.studentList != []:
                student = self.studentList[0]
                self.writeStudent(student)
                self.studentList.remove(student)
        if self.flag == 0 and self.studentList != []:
            for student in self.studentList:
                self.writeStudent(student)
                
        
        
        nowTime = int(time.time())
        self.aim_path = "aim{0}.xls".format(nowTime)
        self.error_path = "error{0}.xls".format(nowTime)
        
        self.aim_wb.save(self.aim_path)
        self.error_wb.save(self.error_path)