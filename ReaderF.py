#coding:utf-8
'''
Created on 2017年6月22日

@author: KB5201314
'''
import urllib
import urllib2
from bs4 import BeautifulSoup
import re


class Reader(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.values = {}
        self.values['dmlx'] = "1"
        self.values['va'] = "UKywzivX"
        self.values['year'] = "1736"
        self.values['ct'] = "1"
        self.values['code'] = None
        self.values['sfzh'] = None
        self.values['yzm'] = "000000"
        
        
    def toDo(self,code,sfzh,s_sid):
        values = self.values
        values['code'] = code
        values['sfzh'] = sfzh
        data = urllib.urlencode(values)
        url = "http://gkcf.jxedu.gov.cn/cjcx/CjQuerySelvet"
        request = urllib2.Request(url,data)
        response = urllib2.urlopen(request)
        if response.getcode() == 200:
            print "学号{0}成功连接".format(s_sid)
            html_doc = response.read().decode('gbk').encode('utf-8')
            #print html_doc
            soup = BeautifulSoup(html_doc,'html.parser',from_encoding = 'utf-8')

            ones = soup.find_all('td')
            print ones
            
            if ones == []:
                print "学号{0}考生号不存在".format(s_sid)
                return None
            else:
                nums = re.findall("\d+", ones[4].get_text())
                print nums
                return nums

        
        else:
            print "学号{0}连接失败".format(s_sid)
            return None
        
        
        
        
        
        
