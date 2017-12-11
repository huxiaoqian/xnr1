# -*- coding: utf-8 -*-
from googletrans import Translator

def translate(q):
    res = []
    try:
        translator = Translator()
        results = translator.translate(q, 'zh-cn')
        for result in results:
            res.append(result.text)
        return res
    except Exception,e:
        print 'Exception: ', str(e)
        return res

if __name__ == '__main__':
    q = ['안녕하세요.', 'Hello world']
    print translate(q)
    