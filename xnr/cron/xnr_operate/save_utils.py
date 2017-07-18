# -*-coding:utf-8-*- 

import os
import sys
import json
reload(sys)
sys.path.append('../../')
from global_utils import es_xnr as es

from global_utils import weibo_hot_content_recommend_results_index_name,\
                            weibo_hot_content_recommend_results_index_type,\
                            weibo_hot_subopinion_results_index_name,weibo_hot_subopinion_results_index_type,\
                            weibo_hot_keyword_task_index_name,weibo_hot_keyword_task_index_type



#use to save results to es
#input: task_id,content_results
#output: status (True/False)


def save_content_recommendation_results(task_id,content_results):

    mark = False

    try:
        item_exist = es.get(index=weibo_hot_content_recommend_results_index_name,\
                            doc_type=weibo_hot_content_recommend_results_index_type,
                            id=task_id)['_source']
        item_exist['task_id'] = task_id
        item_exist['content_recommend'] = json.dumps(content_results)

        es.update(index=weibo_hot_content_recommend_results_index_name,doc_type=weibo_hot_content_recommend_results_index_type,\
                id=task_id,body={'doc':item_exist})

        item_task = dict()
        item_task['compute_status'] = 1  ## 保存内容推荐结果
        es.update(index=weibo_hot_keyword_task_index_name,doc_type=weibo_hot_keyword_task_index_type,\
                    id=task_id,body={'doc':item_task})

    except Exception, e:
        item_exist = dict()
        item_exist['task_id'] = task_id
        item_exist['content_recommend'] = json.dumps(content_results)

        es.index(index=weibo_hot_content_recommend_results_index_name,\
            doc_type=weibo_hot_content_recommend_results_index_type,\
            id=task_id,body=item_exist)

        item_task = dict() 
        item_task['compute_status'] = 1  ## 保存内容推荐结果
        es.update(index=weibo_hot_keyword_task_index_name,doc_type=weibo_hot_keyword_task_index_type,\
                    id=task_id,body={'doc':item_task})

    mark = True

    return mark



#use to save results to es
#input: task_id,opinion_name,word_result,text_list
#output: status (True/False)

def save_subopnion_results(task_id,text_list):

    mark = False

    try:
        item_exist = es.get(index=weibo_hot_subopinion_results_index_name,\
                            doc_type=weibo_hot_subopinion_results_index_type,id=task_id)['_source']

        item_exist['task_id'] = task_id
        item_exist['subopinion_weibo'] = json.dumps(text_list)

        es.update(index=weibo_hot_subopinion_results_index_name,doc_type=weibo_hot_subopinion_results_index_type,\
                    id=task_id,body={'doc':item_exist})


        item_task = dict()
        item_task['compute_status'] = 2  ## 保存内容推荐结果
        es.update(index=weibo_hot_keyword_task_index_name,doc_type=weibo_hot_keyword_task_index_type,\
                    id=task_id,body={'doc':item_task})


    except Exception,e:

        item_exist = dict()
        item_exist['task_id'] = task_id
        item_exist['subopinion_weibo'] = json.dumps(text_list)

        es.index(index=weibo_hot_subopinion_results_index_name,doc_type=weibo_hot_subopinion_results_index_type,\
                    id=task_id,body=item_exist)

        item_task = dict() 
        item_task['compute_status'] = 2  ## 保存子观点结果
        es.update(index=weibo_hot_keyword_task_index_name,doc_type=weibo_hot_keyword_task_index_type,\
                    id=task_id,body={'doc':item_task})

    mark = True

    return mark




