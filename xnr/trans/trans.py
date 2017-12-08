# -*- coding: utf-8 -*-
from google_trans import translate as google_trans
from baidu_trans import translate as baidu_trans
from youdao_trans import translate as youdao_trans

#q为待翻译的语句组成的列表
def trans(q):
    if isinstance(q, list):
        res = google_trans(q)
        if res:
            return res
        else:
            res = baidu_trans(q)
            if res:
                return res
            else:
                res = youdao_trans(q)
                if res:
                    return res
    return False

if __name__ == '__main__':
    q = ['안녕하세요.', 'Hello world','test']
    print trans(q)