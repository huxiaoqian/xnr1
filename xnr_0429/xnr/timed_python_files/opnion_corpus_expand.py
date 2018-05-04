#!/usr/bin/python
#-*- coding:utf-8 -*-
import os
import json
import time
import sys
import gensim

sys.path.append('../')
from global_utils import es_xnr,opinion_corpus_index_name,opinion_corpus_index_type
from parameter import MAX_SEARCH_SIZE,WORD2VEC_PATH

sys.path.append('../cron/opinion_question/')
from opinion_corpus_v2 import get_weibo_text

#step1
def search_expand_task():
    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                        {'term':{'status':0}},
                        ]
                    }
                }
            }
        },
        'size':MAX_SEARCH_SIZE
    }
    try:
        corpus_result = es_xnr.search(index=opinion_corpus_index_name,doc_type=opinion_corpus_index_type,body=query_body)['hits']['hits']
        result_list = []
        for item in corpus_result:
            result_list.append(item['_source'])
    except:
        result_list = []

    return result_list


#step2
def keywords_expand(keywords):
    keywords_list = []
    model = gensim.models.KeyedVectors.load_word2vec_format(WORD2VEC_PATH,binary=True)
    for word in keywords:
        simi_list = model.most_similar(word,topn=5)
        for simi_word in simi_list:
            keywords_list.append(simi_word[0])
    return keywords_list

#step5
def update_opnion_corpus(corpus_id):
    try:
        es_xnr.update(index=opinion_corpus_index_name,doc_type=opinion_corpus_index_type,\
            id=corpus_id,body={'doc':{'status':1}})
        mark = True
    except:
        mark = False

    return mark

###redis
def spcific_opinion_corpus_expand(task):
    origin_keyword = task['corpus_name']
    
    #step2：对领域词进行词扩充
    keywords_list = keywords_expand(origin_keyword)

    #step3:根据师兄算法进行语料扩充与积累
    #step4：将语料积累结果写入文件
    task_mark = get_weibo_text(keywords_list,task['corpus_name'])
    print 'task_mark:',task_mark
    #step5:如果写入文件成功且，则更新状态为1
    if task_mark == 1:
        update_mark = update_opnion_corpus(task['corpus_pinyin'])
    else:
        update_mark = False
    return update_mark    

def opnionn_corpus_expand():
#step1:查询未完成语料库扩充的领域、领域拼音（为存文件做准备）
    corpus_result = search_expand_task()
    update_mark_list = []
    if corpus_result:
        for task in corpus_result:
            print 'task::',task['corpus_name']
            update_mark = spcific_opinion_corpus_expand(task)

            update_mark_list.append(update_mark)

    return update_mark_list




if __name__ == '__main__':
    opnionn_corpus_expand()
