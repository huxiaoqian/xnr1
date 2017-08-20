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
                            weibo_hot_keyword_task_index_name,weibo_hot_keyword_task_index_type,\
                            social_sensing_index_name,social_sensing_index_type



#use to save results to es
#input: task_id,content_results
#output: status (True/False)


def save_content_recommendation_results(task_id,content_results):

    try:
        item_exist = dict()
        item_exist['task_id'] = task_id
        item_exist['content_recommend'] = json.dumps(content_results)
        print '123123123'
        es.index(index=weibo_hot_content_recommend_results_index_name,\
            doc_type=weibo_hot_content_recommend_results_index_type,\
            id=task_id,body=item_exist)
        print '45456456'
        item_task = dict() 
        item_task['compute_status'] = 1  ## 保存内容推荐结果
        es.update(index=weibo_hot_keyword_task_index_name,doc_type=weibo_hot_keyword_task_index_type,\
                    id=task_id,body={'doc':item_task})

        es.update(index=social_sensing_index_name,doc_type=social_sensing_index_type,id=str(json.loads(task_id)),\
                    body={'doc':{'compute_status':1}})
        print '##########'

        mark = True

    except Exception, e:
         mark = False
        
    

    return mark



#use to save results to es
#input: task_id,opinion_name,word_result,text_list
#output: status (True/False)

def save_subopnion_results(task_id,sub_opinion_results):

    #try:
    item_exist = dict()
    item_exist['task_id'] = task_id
    item_exist['subopinion_weibo'] = json.dumps(sub_opinion_results)
    print '33333'
    es.index(index=weibo_hot_subopinion_results_index_name,doc_type=weibo_hot_subopinion_results_index_type,\
                id=task_id,body=item_exist)

    item_task = dict() 
    item_task['compute_status'] = 2  ## 保存子观点结果
    print '111111'
    es.update(index=weibo_hot_keyword_task_index_name,doc_type=weibo_hot_keyword_task_index_type,\
                id=task_id,body={'doc':item_task})
    print '2222'
    item_sensing = dict()
    item_sensing['compute_status'] = 2
    print 'social_sensing_index_name:::',social_sensing_index_name
    print 'social_sensing_index_type:::',social_sensing_index_type
    print 'task_id:::',task_id
    print 'es::',es
    result = es.get(index=social_sensing_index_name,doc_type=social_sensing_index_type,id=str(json.loads(task_id)))
    print 'result:::',result
    es.update(index=social_sensing_index_name,doc_type=social_sensing_index_type,id=str(json.loads(task_id)),\
                body={'doc':item_sensing})
    print '@@@@@@@'

    mark = True

    #except Exception,e:
    #    mark = False
        
    return mark




