# -*-coding:utf-8-*-

import os
import sys
import json
import time

from opnion_corpus_expand import spcific_opinion_corpus_expand
sys.path.append('../')
from global_utils import es_xnr,opinion_corpus_index_name,opinion_corpus_index_type
from global_utils import R_OPINION as r_r
from global_utils import opinion_expand_task_queue_name


## 从redis队列中pop出任务，进行计算
def rpop_expand_opinion_corpus():

    while True:
        temp = r_r.rpop(opinion_expand_task_queue_name)

        # print 'temp:::::',temp
        if not temp:
            print '当前没有观点语料库扩充任务'         
            break
        task_detail = json.loads(temp)
        task_id = task_detail['corpus_pinyin']
        print 'task_detail::',task_detail

        print '把任务从队列中pop出来......'

        spcific_opinion_corpus_expand(task_detail)

        es_xnr.update(index=opinion_corpus_index_name,doc_type=opinion_corpus_index_type,\
            id=task_id, body={'doc':{'status':1}})



if __name__ == '__main__':
    rpop_expand_opinion_corpus()