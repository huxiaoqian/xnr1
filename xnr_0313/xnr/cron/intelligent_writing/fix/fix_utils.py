#-*-coding=utf-8-*-

import os
import errno
import time
import pymongo
#from scws_language.scws_utils import load_scws, cut
from global_utils_do import load_scws, cut

MONGOD_HOST = '219.224.134.212'
MONGOD_PORT = 27017

def _default_mongo(host=MONGOD_HOST, port=MONGOD_PORT, usedb='boat'):
    # 强制写journal，并强制safe
    connection = pymongo.MongoClient(host=host, port=port, j=True, w=1)
    db = connection.admin
    # db.authenticate('root', 'root')
    db = getattr(connection, usedb)
    return db

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def _default_mongo_db(host=MONGOD_HOST, port=MONGOD_PORT):
    # 强制写journal，并强制safe
    connection = pymongo.MongoClient(host=host, port=port, j=True, w=1)
    return connection

def ts2datetime(timestamp):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))

def ts2date(timestamp):
    return time.strftime('%Y%m%d', time.localtime(timestamp))

def datetime2ts(date):
    return int(time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S')))

s = load_scws()
cx_dict = set(['Ag','a','an','Ng','n','nr','ns','nt','nz','Vg','v','vd','vn','@','j']) # 关键词词性词典

EXTRA_BLACK_LIST_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'black.txt')

def load_black_words():
    one_words = set([line.strip('\r\n') for line in file(EXTRA_BLACK_LIST_PATH)])
    return one_words

black_words = load_black_words()

def cut_words(text):
    '''分词, 加入黑名单过滤单个词，保留名词、动词、形容词
       input
           texts: 输入text的list，utf-8
       output:
           terms: 关键词list
    '''
    if not isinstance(text, str):
        raise ValueError("cut words input text must be string")

    cx_terms = cut(s, text, cx=True)

    return [term for term, cx in cx_terms if cx in cx_dict and term not in black_words]
