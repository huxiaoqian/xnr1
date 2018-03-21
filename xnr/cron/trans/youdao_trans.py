#-*- coding: utf-8 -*-
import httplib
import md5
import urllib
import random

appKey = '3026da95302fe406'
secretKey = 'D6Sueb74kdW3nj6qjSaMTGGQTngoHMjW'

def translate(q, target_language):
    res = []
    for item in q:
        r = single_translate(item, target_language)
        if r:
            res.append(r)
        else:
            return False
    return res

def single_translate(q, target_language):
    if target_language == 'zh-cn':
        toLang = 'zh-CHS'
    elif target_language == 'en':
        toLang = 'EN'
    httpClient = None
    myurl = '/api'
    fromLang = 'auto'
    salt = random.randint(1, 65536)
    
    sign = appKey+q+str(salt)+secretKey
    m1 = md5.new()
    m1.update(sign)
    sign = m1.hexdigest()
    myurl = myurl+'?appKey='+appKey+'&q='+urllib.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
     
    try:
        httpClient = httplib.HTTPConnection('openapi.youdao.com')
        httpClient.request('GET', myurl)
        #response是HTTPResponse对象
        response = httpClient.getresponse()
        res = eval(response.read())
        return res['translation'][0].decode('utf8')
    except Exception, e:
        print 'Exception: ', str(e)
        return False
    finally:
        if httpClient:
            httpClient.close()
            

if __name__ == '__main__':
    q = "‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏طالبة جامعية ‏‏من مواليد [١٩٩١م] طموحي الحصول على الدكتوراه في تخصصي من هواياتي: كتابه الخط العربي وعشقي مايسمى [بالتصوير"
    result = single_translate(q, 'zh-cn')
    print result

    