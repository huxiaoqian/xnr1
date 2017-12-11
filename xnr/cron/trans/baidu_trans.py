# -*- coding: utf-8 -*-
import requests
import hashlib
import random
import json

url = 'http://fanyi-api.baidu.com/api/trans/vip/translate'
appid = 20170921000084362
secretKey = 'uKPwOwSfMDG4Byrq1ey7'

def translate(q):
    q = '\n'.join(q)
    salt = random.randint(100000, 999999)
    sign = hashlib.md5(str(appid) + q + str(salt) + secretKey).hexdigest()
    data = {
        'q': q,
        'from': 'auto',
        'to': 'zh',
        'appid': appid,
        'salt': salt,
        'sign':sign
    }
    resp = requests.post(url, data=data).text.encode('utf8')
    results = json.loads(resp)
    res = []
    try:
        for result in results['trans_result']:
            res.append(result['dst'])
        return  res
    except Exception,e:
        print 'Exception: ', str(e)
        return res

if __name__ == '__main__':
    q = "‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏طالبة جامعية ‏‏من مواليد [١٩٩١م] طموحي الحصول على الدكتوراه في تخصصي من هواياتي: كتابه الخط العربي وعشقي مايسمى [بالتصوير"
    result = translate(q)
    print result
