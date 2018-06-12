# coding:utf-8

'''
Created on 2017年9月15日

@author: imlk
'''

import xlrd
from Student import Student


class StudentFactory(object):

    def __init__(self, filePath, startRow, nameColumn, idColumn, sfzhColumn):
        self.filePath = filePath
        self.startRow = startRow
        self.nameColumn = nameColumn
        self.idColumn = idColumn
        self.sfzhColumn = sfzhColumn
        
        self.openFile()
        
    def openFile(self):
        self.sourceExcel = xlrd.open_workbook(self.filePath)
        print u"成功打开了文件{0}".format(self.filePath)
        self.sourceSheet = self.sourceExcel.sheet_by_index(0)
        print u"成功打开了默认工作表"
        self.studentNum = self.sourceSheet.nrows - self.startRow
        print self.studentNum, u"个学生"
        
        self.currentRow = self.startRow
        self.currentStudentNO = 1
    
    def hasNext(self):
        if self.currentRow < self.sourceSheet.nrows: #nows 最长行数
            return True
        else:
            return False
    
    def getNext(self):
        
#         print self.currentStudentNO
        
        student = Student(self.currentStudentNO,
                        self.sourceSheet.cell_value(self.currentRow, self.nameColumn),
                        str(self.sourceSheet.cell_value(self.currentRow, self.idColumn)),
                        str(self.sourceSheet.cell_value(self.currentRow, self.sfzhColumn))
                        )
        
        self.currentRow = self.currentRow + 1
        self.currentStudentNO = self.currentStudentNO + 1
        return student
    
        
