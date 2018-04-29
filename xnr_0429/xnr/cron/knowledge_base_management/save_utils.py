# -*-coding:utf-8-*- 

import os
import sys
reload(sys)
sys.path.append('../../')
from global_utils import es_xnr as es

from global_utils import weibo_domain_index_name,weibo_domain_index_type,\
                        weibo_role_index_name,weibo_role_index_type


#use to save detect results to es
#input: uid list (detect results)
#output: status (True/False)
def save_detect_results(detect_results, decect_task_information):
    mark = False
    task_id = decect_task_information['domain_pinyin']

    try:
        item_exist = es.get(index=weibo_domain_index_name,doc_type=weibo_domain_index_type,id=task_id)['_source']
        item_exist['group_size'] = len(detect_results)
        item_exist['member_uids'] = detect_results
        item_exist['compute_status'] = 1  # 存入uid
        es.update(index=weibo_domain_index_name,doc_type=weibo_domain_index_type,id=task_id,body={'doc':item_exist})
    except Exception, e:
        item_exist = dict()
        item_exist['domain_pinyin'] = json.dumps(decect_task_information['domain_pinyin'])
        item_exist['domain_name'] = json.dumps(decect_task_information['domain_name'])
        item_exist['create_type'] = json.dumps(decect_task_information['create_type'])
        item_exist['create_time'] = decect_task_information['create_time']
        item_exist['submitter'] = json.dumps(decect_task_information['submitter'])
        item_exist['remark'] = json.dumps(decect_task_information['remark'])
        item_exist['group_size'] = len(detect_results)
        item_exist['member_uids'] = detect_results
        item_exist['compute_status'] = 1  # 存入uid
        es.index(index=weibo_domain_index_name,doc_type=weibo_domain_index_type,id=task_id,body=item_exist)
    
    mark = True

    return mark

## 保存群体分析结果

def save_group_description_results(group_results,decect_task_information):
    mark = False   
    task_id = decect_task_information['domain_pinyin']

    try:
        item_exist = es.get(index=weibo_domain_index_name,doc_type=weibo_domain_index_type,id=task_id)['_source']
        item_exist['role_distribute'] = json.dumps(group_results['role_distribute'])
        item_exist['top_keywords'] = json.dumps(group_results['top_keywords'])
        item_exist['political_side'] = json.dumps(group_results['political_side'])
        item_exist['topic_preference'] = json.dumps(group_results['topic_preference'])
        item_exist['compute_status'] = 2  # 存入群体描述
        es.update(index=weibo_domain_index_name,doc_type=weibo_domain_index_type,id=task_id,body={'doc':item_exist})
    except Exception, e:
        item_exist = dict()
        item_exist['domain_pinyin'] = json.dumps(decect_task_information['domain_pinyin'])
        item_exist['domain_name'] = json.dumps(decect_task_information['domain_name'])
        item_exist['create_type'] = json.dumps(decect_task_information['create_type'])
        item_exist['create_time'] = json.dumps(decect_task_information['create_time'])
        item_exist['submitter'] = json.dumps(decect_task_information['submitter'])
        item_exist['remark'] = json.dumps(decect_task_information['remark'])
        item_exist['role_distribute'] = json.dumps(group_results['role_distribute'])
        item_exist['top_keywords'] = json.dumps(group_results['top_keywords'])
        item_exist['political_side'] = json.dumps(group_results['political_side'])
        item_exist['topic_preference'] = json.dumps(group_results['topic_preference'])
        item_exist['compute_status'] = 2  # 存入群体描述
        es.index(index=weibo_domain_index_name,doc_type=weibo_domain_index_type,id=task_id,body=item_exist)
    
    mark = True

    return mark

## 保存角色分析结果

def save_role_feature_analysis(role_results,role_label,domain,role_id,task_id):
    mark = False

    try:
        item_exist = es.get(index=weibo_role_index_name,doc_type=weibo_role_index_type,id=role_id)['_source']
        item_exist['role_pinyin'] = role_id
        item_exist['role_name'] = role_label
        item_exist['domains'] = domain
        item_exist['personality'] = json.dumps(role_results['personality'])
        item_exist['political_side'] = json.dumps(role_results['political_side'])
        item_exist['geo'] = json.dumps(role_results['geo'])
        item_exist['active_time'] = json.dumps(list(role_results['active_time']))
        item_exist['day_post_num'] = json.dumps(list(role_results['day_post_num']))
        

        es.update(index=weibo_role_index_name,doc_type=weibo_role_index_type,id=role_id,body={'doc':item_exist})
    	
    	item_domain = dict()
    	item_domain['compute_status'] = 3  # 存入角色分析结果
    	es.update(index=weibo_domain_index_name,doc_type=weibo_domain_index_type,id=task_id,body={'doc':item_domain})
    
    except Exception, e:
        item_exist = dict()
        item_exist['role_pinyin'] = role_id
        item_exist['role_name'] = role_label
        item_exist['domains'] = domain
        item_exist['personality'] = json.dumps(role_results['personality'])
        item_exist['political_side'] = json.dumps(role_results['political_side'])
        item_exist['geo'] = json.dumps(role_results['geo'])
        item_exist['active_time'] = json.dumps(list(role_results['active_time']))
        item_exist['day_post_num'] = json.dumps(list(role_results['day_post_num']))
       
        es.index(index=weibo_role_index_name,doc_type=weibo_role_index_type,id=role_id,body=item_exist)
        
        item_domain = dict()
    	item_domain['compute_status'] = 3  # 存入角色分析结果
    	es.update(index=weibo_domain_index_name,doc_type=weibo_domain_index_type,id=task_id,body={'doc':item_domain})
    
    mark =True

    return mark
