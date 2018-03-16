# -*- coding:utf-8-*-
import random
import time
import sys
sys.path.append('../')
from global_config import S_TYPE,S_DATE_TW
from global_utils import es_xnr,tw_xnr_fans_followers_index_name,tw_xnr_fans_followers_index_type,\
                    es_flow_text,twitter_flow_text_index_name_pre,flow_text_index_type,\
                    tw_xnr_retweet_timing_list_index_name,tw_xnr_retweet_timing_list_index_type,\
                    tw_xnr_index_name,tw_xnr_index_type,tw_xnr_timing_list_index_name,\
                    tw_xnr_timing_list_index_type
from parameter import MAX_SEARCH_SIZE,RETWEET_START_TS,RETWEET_END_TS,TRACE_FOLLOW_LIST,task_source_ch2en
from utils import tw_uid2nick_name_photo
from twitter_publish_func import tw_retweet,tw_publish
from time_utils import datetime2ts,ts2datetime

# 从流数据中扫描跟踪人物的发帖
def read_tracing_followers_tweet():

    if S_TYPE == 'test':
        query_body = {
            'query':{
                'term':{'xnr_user_no':'TXNR0001'}
            },
            'size':MAX_SEARCH_SIZE
        }
        
    else:
        query_body = {
            'query':{
                'match_all':{}
            },
            'size':MAX_SEARCH_SIZE
        }


    results = es_xnr.search(index=tw_xnr_fans_followers_index_name,doc_type=tw_xnr_fans_followers_index_type,\
                body=query_body)['hits']['hits']
    if results:
        for result in results:
            result = result['_source']
            
            xnr_user_no = result['xnr_user_no']
            trace_follow_list = result['trace_follow_list']
            print 'trace_follow_list:::',trace_follow_list

            if S_TYPE == 'test':
                current_time = datetime2ts(S_DATE_TW)
                #trace_follow_list = TRACE_FOLLOW_LIST
            else:
                current_time = int(time.time())

            current_date = ts2datetime(current_time)

            flow_text_index_name = twitter_flow_text_index_name_pre + current_date

            query_body_flow = {
                'query':{
                    'filtered':{
                        'filter':{
                            'terms':{'uid':trace_follow_list}
                        }
                    }
                },
                'size':MAX_SEARCH_SIZE
            }

            results_flow = es_xnr.search(index=flow_text_index_name,doc_type=flow_text_index_type,\
                            body=query_body_flow)['hits']['hits']

            if results_flow:
                for result_flow in results_flow:
                    
                    result_flow = result_flow['_source']
                    tid = result_flow['tid']

                    #先判断 之前是否已经存过该tid
                    
                    task_id = xnr_user_no + '_' + tid
                    try:
                        # 如果已添加则跳过
                        es_xnr.get(index=tw_xnr_retweet_timing_list_index_name,doc_type=\
                            tw_xnr_retweet_timing_list_index_type,id=task_id)['_source']
                        continue

                    except:
                        # 如果未添加过则加入列表
                        task_detail = {}
                        task_detail['xnr_user_no'] = xnr_user_no
                        task_detail['tid'] = tid
                        task_detail['text'] = result_flow['text']
                        task_detail['uid'] = result_flow['uid']
                        task_detail['nick_name'],task_detail['photo_url'] = tw_uid2nick_name_photo(result_flow['uid'])
                        task_detail['timestamp'] = result_flow['timestamp']
                        task_detail['timestamp_set'] = result_flow['timestamp'] + random.randint(RETWEET_START_TS,RETWEET_END_TS)
                        task_detail['compute_status'] = 0

                        es_xnr.index(index=tw_xnr_retweet_timing_list_index_name,doc_type=\
                            tw_xnr_retweet_timing_list_index_type,body=task_detail,id=task_id)

# 扫描定时转发列表
def retweet_operate_timing():

    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'term':{'compute_status':0}
                }
            }
        }
    }

    results = es_xnr.search(index=tw_xnr_retweet_timing_list_index_name,doc_type=\
                    tw_xnr_retweet_timing_list_index_type,body=query_body)['hits']['hits']
    print 'results..',results
    if results:
        for result in results:
            result = result['_source']
            timestamp_set = result['timestamp_set']

            if timestamp_set <= int(time.time()):

                text = result['text'].encode('utf-8')
                tweet_type = 'trace_follow_tweet'
                xnr_user_no = result['xnr_user_no']
                r_tid = result['tid']
                uid = result['uid']


                es_get_result = es_xnr.get(index=tw_xnr_index_name,doc_type=tw_xnr_index_type,id=xnr_user_no)['_source']

                tw_mail_account = es_get_result['tw_mail_account']
                tw_phone_account = es_get_result['tw_phone_account']
                password = es_get_result['password']
                
                if tw_mail_account:
                    account_name = tw_mail_account
                elif tw_phone_account:
                    account_name = tw_phone_account
                else:
                    return False
                print 'text::',text

                
                mark = tw_retweet(account_name, password, r_tid, uid, text, tweet_type, xnr_user_no)
                print 'mark::',mark
                if mark:
                    task_id = xnr_user_no + '_' + r_tid
                    # item_exist = es_xnr.get(index=tw_xnr_retweet_timing_list_index_name,doc_type=\
                 #        tw_xnr_retweet_timing_list_index_type,id=task_id)['_source']
                    item_exist = {}
                    item_exist['compute_status'] = 1
                    #item_exist['timstamp_post'] = int(time.time())

                    es_xnr.update(index=tw_xnr_retweet_timing_list_index_name,doc_type=\
                        tw_xnr_retweet_timing_list_index_type,id=task_id,body={'doc':item_exist})

                    # # 保存微博
                    # try:
                    #     save_mark = save_to_xnr_flow_text(tweet_type,xnr_user_no,text)
                    # except:
                    #     print '保存微博过程遇到错误！'
                    #     save_mark = False
            else:
                continue
        #return mark

# 扫描定时发布列表
def publish_operate_timing():

    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'term':{'task_status':0}
                }
            }
        },
        'size':MAX_SEARCH_SIZE
    }

    results = es_xnr.search(index=tw_xnr_timing_list_index_name,doc_type=\
                    tw_xnr_timing_list_index_type,body=query_body)['hits']['hits']
    #print 'results::',results
    if results:
        for result in results:
            _id = result['_id']
            result = result['_source']
            timestamp_set = result['post_time']
            print timestamp_set
            if timestamp_set <= int(time.time()):
                print '!!'
                text = result['text'].encode('utf-8')
                tweet_type = task_source_ch2en[result['task_source']]
                xnr_user_no = result['xnr_user_no']

                # try:
                #     p_url = result['p_url']
                # except:
                #     p_url = ''
                # try:
                #     rank = result['rank']
                # except:
                #     rank = u'0'
                # try:
                #     rankid = result['rankid']
                # except:
                #     rankid = ''
                #r_tid = result['tid']

                es_get_result = es_xnr.get(index=tw_xnr_index_name,doc_type=tw_xnr_index_type,id=xnr_user_no)['_source']

                tw_mail_account = es_get_result['tw_mail_account']
                tw_phone_account = es_get_result['tw_phone_account']
                password = es_get_result['password']
                
                if tw_mail_account:
                    account_name = tw_mail_account
                elif tw_phone_account:
                    account_name = tw_phone_account
                else:
                    return False
                        
                mark = tw_publish(account_name, password, text, tweet_type, xnr_user_no)

                if mark:
                    #task_id = xnr_user_no + '_' + r_tid
                    task_id = _id
                    # item_exist = es_xnr.get(index=tw_xnr_retweet_timing_list_index_name,doc_type=\
                    #        tw_xnr_retweet_timing_list_index_type,id=task_id)['_source']
                    item_exist = {}
                    item_exist['task_status'] = 1
                    #item_exist['timstamp_post'] = int(time.time())

                    es_xnr.update(index=tw_xnr_timing_list_index_name,doc_type=\
                        tw_xnr_timing_list_index_type,id=task_id,body={'doc':item_exist})

            else:
                continue
        #return mark


if __name__ == '__main__':

    # 定时发帖
    #publish_operate_timing()

    # 定时跟踪转发
    read_tracing_followers_tweet()
    retweet_operate_timing()


