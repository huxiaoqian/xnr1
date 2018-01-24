# -*-coding:utf-8-*- 

import os
import sys
import json
reload(sys)
sys.path.append('../../')
from global_utils import es_xnr as es

from global_utils import tw_hot_content_recommend_results_index_name,\
                            tw_hot_content_recommend_results_index_type,\
                            tw_hot_subopinion_results_index_name,tw_hot_subopinion_results_index_type,\
                            tw_hot_keyword_task_index_name,tw_hot_keyword_task_index_type,\
                            social_sensing_index_type

#use to save results to es
#input: task_id,content_results
#output: status (True/False)

def save_content_recommendation_results(xnr_user_no,mid,task_id,content_results):

    #try:
    item_exist = dict()
    item_exist['xnr_user_no'] = xnr_user_no
    item_exist['mid'] = mid
    item_exist['content_recommend'] = json.dumps(content_results)
    print '123123123'
    es.index(index=tw_hot_content_recommend_results_index_name,\
        doc_type=tw_hot_content_recommend_results_index_type,\
        id=task_id,body=item_exist)
    print '45456456'
    print 'mid:::',mid
    print 'task_id::',task_id
    item_task = dict() 
    item_task['compute_status'] = 1  ## 保存内容推荐结果
    es.update(index=tw_hot_keyword_task_index_name,doc_type=tw_hot_keyword_task_index_type,\
                id=task_id,body={'doc':item_task})

    es.update(index=social_sensing_index_name,doc_type=social_sensing_index_type,id=mid,\
                body={'doc':{'compute_status':1}})
    print '##########'

    mark = True

    # except Exception, e:
    #      mark = False

    return mark



#use to save results to es
#input: task_id,opinion_name,word_result,text_list
#output: status (True/False)

def save_subopnion_results(xnr_user_no,mid,task_id,sub_opinion_results):
    
    #try:
    item_exist = dict()
    item_exist['xnr_user_no'] = xnr_user_no
    item_exist['mid'] = mid
    item_exist['subopinion_tw'] = json.dumps(sub_opinion_results)
    #print 'sub_opinion_results::',sub_opinion_results

    es.index(index=tw_hot_subopinion_results_index_name,doc_type=tw_hot_subopinion_results_index_type,\
                id=task_id,body=item_exist)

    item_task = dict() 
    item_task['compute_status'] = 2  ## 保存子观点结果
    print 'tw_hot_keyword_task_index_name...',tw_hot_keyword_task_index_name

    es.update(index=tw_hot_keyword_task_index_name,doc_type=tw_hot_keyword_task_index_type,\
                id=task_id,body={'doc':item_task})

    mark = True

    #except Exception,e:
    #    mark = False
        
    return mark




