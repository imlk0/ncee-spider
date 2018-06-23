# coding:utf-8

'''
Created on 2017年9月15日

@author: imlk
'''
from StudentFactory import StudentFactory
from Getter import Getter
from Writter import Writter
from LogUtil import LogUtil

if __name__ == "__main__":
    
    THREAD_NUM_MAX = 30
    
    logUtil = LogUtil()
    
    studentFactory = StudentFactory('book5.xls', startRow=1, nameColumn=0, idColumn=1, sfzhColumn=2)
    if studentFactory.studentNum == 0: #
        exit()
    getterList = [Getter(i, logUtil) for i in range(studentFactory.studentNum if studentFactory.studentNum < THREAD_NUM_MAX else THREAD_NUM_MAX)]
    for getter in getterList:
        getter.start()
    writter = Writter(studentFactory.studentNum, logUtil)
    writter.start()
    while studentFactory.hasNext():
        
        for getter in getterList:
            if getter.flag == 1: # 正在运行
                continue
            elif getter.flag == 2:# 一次任务结束
                writter.addStudent(getter.getStudent())
                getter.flag = 0
                
            if getter.flag == 0:# 空闲
                getter.setStudent(studentFactory.getNext())
                getter.flag = 1  # 启动
                break
    
    for getter in getterList:
        getter.exit = 1  # 通知准备退出
        getter.join()

        if getter.hasResolvedStudent():        
            writter.addStudent(getter.getStudent())
            
    writter.flag = 0
    writter.join()
