# -*- coding: utf-8 -*-
from googletrans import Translator

def translate(q, target_language):
    res = []
    try:
        translator = Translator()
        results = translator.translate(q, target_language)
        for result in results:
            res.append(result.text)
        return res
    except Exception,e:
        print 'Exception: ', str(e)
        return res

if __name__ == '__main__':
    q = ['Hello world']
    for r in translate(q, 'zh-cn'):
        print r
