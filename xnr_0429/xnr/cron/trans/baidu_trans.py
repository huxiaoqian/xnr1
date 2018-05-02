# -*- coding: utf-8 -*-
import requests
import hashlib
import random
import json

url = 'http://fanyi-api.baidu.com/api/trans/vip/translate'
appid = 20170921000084362
secretKey = 'uKPwOwSfMDG4Byrq1ey7'

def translate(q, target_language):
    if target_language == 'zh-cn':
        target_lang = 'zh'
    elif target_language == 'en':
        target_lang = 'en'
    q = '\n'.join(q)
    salt = random.randint(100000, 999999)
    sign = hashlib.md5(str(appid) + q + str(salt) + secretKey).hexdigest()
    data = {
        'q': q,
        'from': 'auto',
        'to': target_lang,
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

    q = "‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏‏안녕하세요"
    result = translate(q, 'zh-cn')
    print result
