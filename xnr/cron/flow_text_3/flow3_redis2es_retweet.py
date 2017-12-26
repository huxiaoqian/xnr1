# -*- coding=utf-8 -*-
'''
use to scan redis(retweet/be_retweet) to insert es
'''
import sys
import time
import json
import redis

reload(sys)
sys.path.append('../../')
from global_utils import es_xnr as es
from global_utils import R_retweet, fb_retweet_dict, tw_retweet_dict, redis_host_list
from global_config import R_BEGIN_TIME, S_TYPE
from parameter import DAY
from time_utils import ts2datetime, datetime2ts
from be_retweet_network_mappings import be_retweet_es_mappings


begin_ts = datetime2ts(R_BEGIN_TIME)


#use to get db_number which is needed to es
def get_db_num(timestamp):
    date = ts2datetime(timestamp)
    date_ts = datetime2ts(date)
    db_number = 2 - (((date_ts - begin_ts) / (DAY * 7))) % 2
    #run_type
    if S_TYPE == 'test':
        db_number = 1
    return db_number


#use to get db retweet/be_retweet redis to es
def scan_retweet(ft_type):
    count = 0
    scan_cursor = 0
    now_ts = time.time()
    now_date_ts = datetime2ts(ts2datetime(now_ts))
    #get redis db number
    db_number = get_db_num(now_date_ts)

    if ft_type == 'fb':
        retweet_redis_dict = fb_retweet_dict
        index_name = 'fb_be_retweet_' +str(db_number)
    else:
        retweet_redis_dict = tw_retweet_dict
        index_name = 'tw_be_retweet_' +str(db_number)

    #get redis db
    retweet_redis = retweet_redis_dict[str(db_number)]

    # # 1. 判断即将切换的db中是否有数据
    # while 1:
    #     redis_host_list.pop(db_number)
    #     other_db_number = retweet_redis_dict[redis_host_list[0]] # 获得对应的redis
    #     current_dbsize = other_db_number.dbsize()
    #     if current_dbsize:
    #         break # 已经开始写入新的db，说明前一天的数据已经写完
    #     else:
    #         time.sleep(60)

    # 2. 删除之前的es
    
    be_retweet_es_mappings(str(db_number),ft_type)
    
    
    # 3. scan

    retweet_bulk_action = []
    be_retweet_bulk_action = []
    start_ts = time.time()
    #retweet count/be_retweet count
    #retweet_count = 0
    be_retweet_count = 0
    while True:
        re_scan = retweet_redis.scan(scan_cursor, count=100)
        re_scan_cursor = re_scan[0]
        '''
        if re_scan_cursor == 0:
            print 'scan finish'
            if retweet_bulk_action != []:
                es.bulk(retweet_bulk_action, index='retweet_'+str(db_number), doc_type='user')
            if be_retweet_bulk_action != []:
                es.bulk(be_retweet_bulk_action, index='be_retweet_'+str(db_number), doc_type='user')
            break
        '''
        for item in re_scan[1]:
            count += 1
            item_list = item.split('_')
            save_dict = {}
           
            if len(item_list)==3:
                be_retweet_count += 1
                uid = item_list[2]
                item_result = retweet_redis.hgetall(item)
                save_dict['uid'] = uid
                save_dict['uid_be_retweet'] = json.dumps(item_result)
                be_retweet_bulk_action.extend([{'index':{'_id':uid}}, save_dict])
        print 'be_retweet_bulk_action...',be_retweet_bulk_action
        es.bulk(be_retweet_bulk_action, index=index_name, doc_type='user')
        retweet_bulk_action = []
        be_retweet_bulk_action = []
        end_ts = time.time()
        print '%s sec scan %s count user:', (end_ts - start_ts, count)
        start_ts = end_ts
        scan_cursor = re_scan[0]
        if scan_cursor==0:
            break
    print 'count:', count

    
    # flushdb

    retweet_redis.flushdb()
    
    print 'end'

if __name__ == '__main__':

    ft_type = 'fb' #'tw'
    scan_retweet(ft_type)