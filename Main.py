#coding:utf-8

'''
Created on 2017年6月22日

@author: KB5201314
'''
import xlrd


import xlwt
#from com.HaHa.ScoreRecorder.
from ReaderF import Reader
import time




if __name__ == '__main__':
    
    filename = raw_input("原始文件路径：") #原始文件
    #"book1.xls"
    #/storage/emulated/0/qpython/scripts/ScoreRecorder/com/HaHa/ScoreRecorder/
    #
    #
    sourceExcel = xlrd.open_workbook(filename)

    print "成功打开了文件{0}".format(filename)
    sourceSheet = sourceExcel.sheet_by_index(0)
    print "成功打开了工作表"
    
    firstID = ####### #首个考生号
    
    
    studentNum = ##  #班级人数
    IDs = range(firstID,firstID + studentNum)
    name = []
    sfzh = []
    count = 0
    while count < studentNum:
        #print sourceSheet.cell_value(count + 1,0)
        name.append(sourceSheet.cell_value(count + 1,0))
        #print sourceSheet.cell_value(count + 1,1)[14:18]
        sfzh.append(sourceSheet.cell_value(count + 1,1)[14:18])#填充所有人按学号的身份证号
        count = count + 1
    
    aim_wb = xlwt.Workbook()
    
    aim_sh = aim_wb.add_sheet("Sheet1")
    aim_sh.write(0, 0,u'姓名')
    aim_sh.write(0, 1,u'本科总分(含加分)')
    aim_sh.write(0, 2,u'本科排名')
    aim_sh.write(0, 3,u'专科总分(含加分)')
    aim_sh.write(0, 4,u'专科排名')
    aim_sh.write(0, 5,u'语文')
    aim_sh.write(0, 6,u'数学')
    aim_sh.write(0, 7,u'外语')
    aim_sh.write(0, 8,u'综合')
    aim_sh.write(0, 9,u'技术')
    
    
    Areader = Reader()
    count = 0
    while count < studentNum:
        print str(IDs[count])[4:19]
        nums = Areader.toDo( str(IDs[count])[4:19],sfzh[count],count + 1)
        if nums is not None:
            
            
            aim_sh.write(count + 1, 0,name[count])
            
            
            aim_sh.write(count + 1, 1,nums[2])
            aim_sh.write(count + 1, 2,nums[3])
            aim_sh.write(count + 1, 3,nums[4])
            aim_sh.write(count + 1, 4,nums[5])
            aim_sh.write(count + 1, 5,nums[6])
            aim_sh.write(count + 1, 6,nums[7])
            aim_sh.write(count + 1, 7,nums[8])
            aim_sh.write(count + 1, 8,nums[9])
            aim_sh.write(count + 1, 9,nums[10])

        
        count = count +1

    aim_wb.save("aim{0}.xls".format(int(time.time())))
#/storage/emulated/0/qpython/scripts/ScoreRecorder/com/HaHa/ScoreRecorder/
def getScore(ID,sfzh,s_sid):
    Areader = Reader()
    dic = Areader.toDo(ID,sfzh,s_sid)
    if nums is not None:
        print nums
    
    
