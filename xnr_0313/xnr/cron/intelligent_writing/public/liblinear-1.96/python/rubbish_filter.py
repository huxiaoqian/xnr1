# -*- coding: utf-8 -*-

import os
import scws
import time
import csv
import re
from gensim import corpora
#from xapian_case.utils import load_scws, cut, cut_filter
from global_utils_do import load_scws, cut, cut_filter
from liblinearutil import svm_read_problem, load_model, predict, save_model, train

sw = load_scws()

AB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), './')
FEATURE_WORD_PATH = os.path.join(AB_PATH, './svm/dictionary_20150124.txt')
SVM_MODEL_FILE = os.path.join(AB_PATH, './svm/train.model')
TRAIN_DATA_FILE = os.path.join(AB_PATH, './train20150124.csv')
TRAIN_INPUT_FILE = os.path.join(AB_PATH, './svm/train20150124.txt')

dictionary = corpora.Dictionary.load_from_text(FEATURE_WORD_PATH)

def prepare_svm_input_file(texts, dictionary=dictionary):
    """将svm输入处理成文件
    """
    pid = os.getpid()
    svm_input_path = os.path.join(AB_PATH, './svm_test/%s.txt' % pid)

    fw = open(svm_input_path, 'w')
    for text in texts:
        words = cut(sw, text)
        feature = dictionary.doc2bow(words)
        line = '1 ' + ' '.join([str(wordid + 1) + ':' + str(wordcount) for wordid, wordcount in feature])
        fw.write('%s\n' % line)
    fw.close()

    return svm_input_path


def prepare_svm_input(texts, y=None, dictionary=dictionary):
    """处理svm输入
    """
    x = []

    if not y:
        y = [1.0 for i in range(0, len(texts))]

    for text in texts:
        words = cut(sw, text)
        feature = dictionary.doc2bow(words)
        x.append(dict(feature))

    return y, x


def train_model():
    """训练模型
    """
    y, x = svm_read_problem(TRAIN_INPUT_FILE)
    m = train(y, x, '-c 4')
    save_model(SVM_MODEL_FILE, m)


def liblinear_classifier(svm_input=None, y=[], x=[]):
    """调用训练好的liblinear分类器做垃圾过滤
    """
    svm_model = load_model(SVM_MODEL_FILE)

    if svm_input:
        y, x = svm_read_problem(svm_input)

    p_label, p_acc, p_val = predict(y, x, svm_model, "-q")

    return p_label


def rubbish_filter(weibos):
    """
    垃圾过滤主函数：
    输入数据:weibo(list元素)，示例：[{'id', 'text',...}]
    text为utf-8编码
    输出数据:(list元素)，示例：[{'rub_label':类别标签},{'rub_label':类别标签}...]
            1表示垃圾文本，0表示非垃圾文本
    """
    results = []
    candidate_weibos = []
    candidate_mids = []
    candidate_texts = []
    for weibo in weibos:
        label = 0
        mid = weibo['id']
        text = weibo['content168']

        if text == '转发微博':
            weibo['rub_label'] = 1
            results.append(weibo)
        else:
            candidate_weibos.append(weibo)
            candidate_mids.append(mid)
            candidate_texts.append(text)

    y, x = prepare_svm_input(candidate_texts)
    labels = liblinear_classifier(y=y, x=x)
    mid_labels = dict(zip(candidate_mids, labels))

    for weibo in candidate_weibos:
        weibo['rub_label'] = int(mid_labels[weibo['id']])
        results.append(weibo)

    return results


if __name__=="__main__":
    train_model()
