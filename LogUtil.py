# coding:utf-8

'''
Created on 2017年9月16日

@author: imlk
'''

import threading
import sys


class LogUtil(object):

    def __init__(self):
        self.lastFlag = 1
        self.lastMsg = ''
        self.lock=threading.Lock()


    def mprint(self, flag, msg):
        
        self.lock.acquire()
        
        if flag == 1:
            if self.lastFlag == 1:
                
                print msg
                
            elif self.lastFlag == 0:
                sys.stdout.write(' ' * len(self.lastMsg) + '\r')
                sys.stdout.flush()
            
                print msg
            
                sys.stdout.write(self.lastMsg + '\r')
                sys.stdout.flush()
                
            
        if flag == 0:
            sys.stdout.write(' ' * len(self.lastMsg) + '\r')
            sys.stdout.flush()
            
            sys.stdout.write(msg + '\r')
            sys.stdout.flush()
                
                
        self.lastMsg = msg
        self.lastFlag = flag

        self.lock.release()

