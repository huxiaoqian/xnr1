# -*- coding: utf-8 -*-
import json
import time
import redis
import elasticsearch
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, scan
from sensitive.get_sensitive import get_sensitive_info,get_sensitive_user
import sys
sys.path.append('../../')
from utils import uid2xnr_user_no,save_to_fans_follow_ES,judge_sensing_sensor,judge_trace_follow
from global_utils import es_xnr as es
from global_utils import R_WEIBO_XNR_FANS_FOLLOWERS as r_fans_follows 
from global_utils import r_fans_uid_list_datetime_pre,r_fans_count_datetime_xnr_pre,r_fans_search_xnr_pre,\
                r_followers_uid_list_datetime_pre,r_followers_count_datetime_xnr_pre,r_followers_search_xnr_pre
from weibo_feedback_mappings import weibo_feedback_retweet_mappings,weibo_feedback_comment_mappings,\
                            weibo_feedback_at_mappings,weibo_feedback_like_mappings,\
                            weibo_feedback_private_mappings

#es = Elasticsearch("http://219.224.134.213:9205/")

def save_to_redis_fans_follow(uid_xnr,uid,save_item):

    current_time = int(time.time())
    datetime = ts2datetime(current_time)
    if save_item == 'fans':
        r_uid_list_datetime_pre = r_fans_uid_list_datetime_pre
        r_count_datetime_xnr_pre = r_fans_count_datetime_xnr_pre
        r_search_xnr_pre = r_fans_search_xnr_pre
    else:
        r_uid_list_datetime_pre = r_followers_uid_list_datetime_pre
        r_count_datetime_xnr_pre = r_followers_count_datetime_xnr_pre
        r_search_xnr_pre = r_followers_search_xnr_pre

    r_uid_list_datetime_index_name = r_uid_list_datetime_pre + datetime
    r_count_datetime_xnr_index_name = r_count_datetime_xnr_pre + datetime + '_' + uid_xnr
    r_search_xnr_index_name = r_search_xnr_pre + uid_xnr

    exist_item = r_fans_follows.hexists(r_search_xnr_index_name,uid)
    if not exist_item:
        try:
            get_result = r_fans_follows.hget(r_uid_list_datetime_index_name,uid_xnr)
            uid_list = json.loads(get_result)
            uid_list.append(uid)
            uid_list = json.dumps(uid_list)


            r_fans_follows.hset(r_uid_list_datetime_index_name,uid_xnr,uid_list)
            r_fans_follows.hset(r_search_xnr_index_name,uid,datetime)
        except:
            uid_list = json.dumps([uid])
            r_fans_follows.hset(r_uid_list_datetime_index_name,uid_xnr,uid_list)
            r_fans_follows.hset(r_search_xnr_index_name,uid,datetime)

        try:
            r_fans_follows.incr(r_count_datetime_xnr_index_name)
            
        except:
            r_fans_follows.set(r_count_datetime_xnr_index_name,'0')


def executeES(indexName, typeName, listData):
    #current_time = int(time.time())
    #indexName += '_' + ts2datetime(current_time)
    
    #print 'listData:',listData
    for list_data in listData:
        
        data = {}
        jsonData = json.loads(list_data)
        for key, val in jsonData.items():
            # print key, '====', val
            data[key] = val
            # data['update_time'] = current_time

        
        if indexName != 'weibo_feedback_group':
            
            xnr_user_no = uid2xnr_user_no(data["root_uid"])

            sensor_mark = judge_sensing_sensor(xnr_user_no,data['uid'])
            data['sensor_mark'] = sensor_mark

            trace_follow_mark = judge_trace_follow(xnr_user_no,data['uid'])
            data['trace_follow_mark'] = trace_follow_mark

            data['sensitive_info'] = get_sensitive_info(data['timestamp'],data['mid'])
            data['sensitive_user'] = get_sensitive_user(data['uid'])


            if indexName == 'weibo_feedback_follow':
                # 修改 _id、保存至fans_followers_es表
                _id = data["root_uid"]+'_'+data["mid"]
                xnr_user_no = uid2xnr_user_no(data["root_uid"])
                
                save_type = 'followers'
                follow_type = 'follow'

                if xnr_user_no:      
                    save_to_fans_follow_ES(xnr_user_no,data["uid"],save_type,follow_type)
                    save_to_redis_fans_follow(xnr_user_no,data["uid"],save_type)

                    # sensor_mark = judge_sensing_sensor(xnr_user_no,data['uid'])
                    # data['sensor_mark'] = sensor_mark

                    # trace_follow_mark = judge_trace_follow(xnr_user_no,data['uid'])
                    # data['trace_follow_mark'] = trace_follow_mark
                print 'save to es!!!!',es.index(index=indexName, doc_type=typeName, id=_id, body=data)

            elif indexName == 'weibo_feedback_fans':
                _id = data["root_uid"]+'_'+data["mid"]
                xnr_user_no = uid2xnr_user_no(data["root_uid"])
                save_type = 'fans'
                follow_type = 'follow'
                
                if xnr_user_no:
                    save_to_fans_follow_ES(xnr_user_no,data["uid"],save_type,follow_type)
                    save_to_redis_fans_follow(xnr_user_no,data["uid"],save_type)
                    
                    # sensor_mark = judge_sensing_sensor(xnr_user_no,data['uid'])
                    # data['sensor_mark'] = sensor_mark

                    # trace_follow_mark = judge_trace_follow(xnr_user_no,data['uid'])
                    # data['trace_follow_mark'] = trace_follow_mark
		try:
		    es.get(index=indexName,doc_type=typeName,id=_id)
		except:
                    print 'save to es!!!!',es.index(index=indexName, doc_type=typeName, id=_id, body=data)
            
            elif indexName == 'weibo_feedback_comment':
                indexName_date =indexName + '_' + ts2datetime(data['timestamp'])
                date_time = ts2datetime(data['timestamp'])
                # print 'date!!!!!!!',date_time
                # print 'indexName_date:::',indexName_date
                mappings_func = weibo_feedback_comment_mappings
                _id = data["mid"]
                # print 'comment_id........',_id
                mappings_func(date_time)
                # print 'data:::',data
                print 'save to es!!!!',es.index(index=indexName_date, doc_type=typeName, id=_id, body=data)

            elif indexName == 'weibo_feedback_retweet':
                # indexName += '_' + ts2datetime(data['timestamp'])
                indexName_date =indexName + '_' + ts2datetime(data['timestamp'])

                date_time = ts2datetime(data['timestamp'])

                mappings_func = weibo_feedback_retweet_mappings
                _id = data["mid"]
                mappings_func(date_time)
                print 'save to es!!!!',es.index(index=indexName_date, doc_type=typeName, id=_id, body=data)

            elif indexName == 'weibo_feedback_at':
                # indexName += '_' + ts2datetime(data['timestamp'])
                indexName_date =indexName + '_' + ts2datetime(data['timestamp'])

                date_time = ts2datetime(data['timestamp'])
                
                mappings_func = weibo_feedback_at_mappings
                _id = data["mid"]
                mappings_func(date_time)
                print 'save to es!!!!',es.index(index=indexName_date, doc_type=typeName, id=_id, body=data)

            elif indexName == 'weibo_feedback_like':
                # indexName += '_' + ts2datetime(data['timestamp'])
                indexName_date =indexName + '_' + ts2datetime(data['timestamp'])

                date_time = ts2datetime(data['timestamp'])

                mappings_func = weibo_feedback_like_mappings
                _id = data["mid"]
                mappings_func(date_time)
                print 'save to es!!!!',es.index(index=indexName_date, doc_type=typeName, id=_id, body=data)

            elif indexName == 'weibo_feedback_private':
                # indexName += '_' + ts2datetime(data['timestamp'])
                indexName_date =indexName + '_' + ts2datetime(data['timestamp'])

                date_time = ts2datetime(data['timestamp'])
                mappings_func = weibo_feedback_private_mappings
                _id = data["mid"]
                mappings_func(date_time)
                print 'save to es!!!!',es.index(index=indexName_date, doc_type=typeName, id=_id, body=data)

        else:
        
            _id = data["mid"]
            print 'save to es!!!!',es.index(index=indexName, doc_type=typeName, id=_id, body=data)

        # print 'data.........',data
        # print 'indexName....',indexName
        # print '_id......',_id
        # #print 'typeName.....',typeName
        # print 'es...',es

        # print 'save to es!!!!',es.index(index=indexName, doc_type=typeName, id=_id, body=data)

    print 'update %s ES done' % indexName

def ts2datetime(ts):
    return time.strftime('%Y-%m-%d', time.localtime(ts))

