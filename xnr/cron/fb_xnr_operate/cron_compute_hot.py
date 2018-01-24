# -*-coding:utf-8-*-

import os
import json
import time

from save_utils import save_content_recommendation_results,save_subopnion_results


# # 引入内容推荐分类器
# from content_recommend.process_summary import summary_main

# 引入子观点分析分类器
import sys
sys.path.append('/home/ubuntu8/yuanhuiru/xnr/xnr1/xnr/cron/xnr_operate/sub_opinion_analysis/')
from opinion_produce import opinion_main

import sys
reload(sys)
sys.path.append('../../')

from global_utils import es_xnr as es
from global_utils import fb_recommend_subopinion_keywords_task_queue_name as keyword_task_queue_name
from global_utils import R_RECOMMEND_SUBOPINION_KEYWORD_TASK as r
from global_utils import fb_hot_keyword_task_index_name,fb_hot_keyword_task_index_type,\
                        fb_recommend_subopinion_keywords_task_queue_name,\
                        fb_xnr_fans_followers_index_name,fb_xnr_fans_followers_index_type
from global_config import S_TYPE,S_DATE_FB
from time_utils import fb_get_flow_text_index_list,datetime2ts
from parameter import MAX_SEARCH_SIZE,SUB_OPINION_WEIBO_LIMIT

#use to add task to redis queue when the task  detect process fail
#input: decect_task_information
#output: status
def add_task_2_queue(queue_name,task_information):
    status = True
    try:
        r.lpush(queue_name,json.dumps(task_information))
    except:
        status = False

    return status


## 从redis队列中pop出任务，进行计算

def rpop_compute_recommend_subopnion():

    while True:
        temp = r.rpop(keyword_task_queue_name)

        print 'temp:::::',temp
        if not temp:
            print '当前没有内容推荐和子观点分析的关键词任务'         
            break
        task_detail = json.loads(temp)
        #print 'task_detail::',task_detail

        print '把任务从队列中pop出来......'

        compute_recommend_subopnion(task_detail)


## 根据关键词，提取微博，并进行内容推荐和子观点分析计算
## input: task_dict {'task_id': ,'keywords_string': }

def compute_recommend_subopnion(task_detail):

    print '开始分析计算......'

    task_id = task_detail['task_id'].strip('"')
    
    keywords_string = task_detail['keywords_string']

    keywords_list = keywords_string.split('&')  ## 以 & 切分关键词，得到list

    xnr_user_no = task_detail['xnr_user_no']
    mid = task_detail['mid']

    query_item = 'keywords_string'
    nest_query_list = []
    for keyword in keywords_list:
        nest_query_list.append({'wildcard':{query_item:'*'+keyword+'*'}})
    
    '''
    ## 重点关注当前虚拟人的关注用户
    if S_TYPE == 'test':
        # followers_list = get_result['followers_list']
        # nest_query_list.append({'terms':followers_list})
        print '全部用户'
    else:
        get_result = es.get(index=fb_xnr_fans_followers_index_name,doc_type=fb_xnr_fans_followers_index_type,\
        id=xnr_user_no)['_source']
        followers_list = get_result['followers_list']
        nest_query_list.append({'terms':followers_list})
    '''

    if S_TYPE == 'test':
        create_time = datetime2ts(S_DATE_FB)
    else:
        create_time = datehour2ts(ts2datehour(time.time()-3600))
    
    #fb_get_flow_text_index_list(create_time)
    
    #index_name_list_list = fb_get_flow_text_index_list(now_timestamp)
    index_name_list = fb_get_flow_text_index_list(create_time)
    print 'index_name_list::',index_name_list
    es_results = es.search(index=index_name_list,doc_type='text',\
                    body={'query':{'bool':{'must':nest_query_list}},'size':MAX_SEARCH_SIZE})['hits']['hits']

    fb_list = [] ## 内容推荐和子观点分析的输入
    
    if es_results:
        for item in es_results:
            item = item['_source']
            fb = item['text']
            fb_list.append(fb)
    
    ## 内容推荐

    ## 得到推荐句子列表
    #print 'fb_list::::::',fb_list
    # print '开始内容推荐计算......'
    # if fb_list:
    #     content_results = summary_main(fb_list)
    # else:
    #     content_results = []

    # print '开始保存内容推荐计算结果......'

    # mark = save_content_recommendation_results(xnr_user_no,mid,task_id.encode('utf-8'),content_results)
    # print 'mark_content:::',mark
    # if mark == False:
    #     print '内容推荐结果保存过程中遇到错误，把计算任务重新push到队列中'
    #     add_task_2_queue(keyword_task_queue_name,task_detail)
    # else:
    #     print '内容推荐计算结果保存完毕......'
    
    ## 子观点分析
    '''
    输入：
    fb_data：微博列表，[fb1,fb2,...]
    k_cluster：子话题个数 （默认为5）
    输出：
    opinion_name：子话题名称字典，{topic1:name1,topic2:name2,...}
    word_result：子话题关键词对，{topic1:[w1,w2,...],topic2:[w1,w2,...],...}
    text_list：子话题对应的文本，{topic1:[text1,text2,...],topic2:[text1,text2,..],..}
    '''
    
    print '开始子观点计算......'
    if fb_list:
        opinion_name,word_result,text_list = opinion_main(fb_list,k_cluster=5)
        sub_opinion_results = dict()

        for topic, text in text_list.iteritems():
            
            topic_name = opinion_name[topic]
            sub_opinion_results[topic_name] = text[:SUB_OPINION_WEIBO_LIMIT]
            
    else:
        sub_opinion_results = {}

    print '开始保存子观点计算结果......'
    mark = save_subopnion_results(xnr_user_no,mid,task_id,sub_opinion_results)
    print 'mark_opinion:::',mark
    if mark == False:

        print '子观点计算结果保存过程中遇到错误，把计算任务重新push到队列中'

        add_task_2_queue(keyword_task_queue_name,task_detail)

    else:
        print '子观点计算结果保存完毕......'





