# coding=utf-8


import time            
import re            
import os    
import sys
import csv
import urllib
import urllib2
import chardet

REQURL = 'http://www.tuling123.com/openapi/api'
API_KEY = 'd179b7e3170e437ea5c6eb14f7b7caf9'

def get_message_from_tuling(massage):#从图灵机器人获取回复

    if not isinstance(massage, str):
        return 'Wrong Coding!!'
    
    test_data = {'key':API_KEY,'info':massage,'userid':'yuanshi'}
    test_data_urlencode = urllib.urlencode(test_data)
    req = urllib2.Request(url = REQURL,data =test_data_urlencode)

    res_data = urllib2.urlopen(req)
    res = res_data.read()
    result = eval(res)
    return result['text']


if __name__ == '__main__':

    result = get_message_from_tuling('我们只是在表达民意[喵喵]')
    print result
