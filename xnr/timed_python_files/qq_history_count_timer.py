# -*-coding:utf-8-*-
import time
import json
import os
import sys
sys.path.append('../')
from global_utils import qq_xnr_history_count_index_name,qq_xnr_history_count_index_type,es_xnr as es,\
                group_message_index_name_pre,group_message_index_type,qq_xnr_index_name,\
                qq_xnr_index_type

from time_utils import ts2datetime,datetime2ts
from parameter import DAY,MAX_VALUE

def qq_history_count(xnr_user_no,qq_number,current_time):

    current_date = ts2datetime(current_time)
    timestamp = datetime2ts(current_date)
    last_date = ts2datetime(current_time-DAY)
    print 'current_date:::',current_date

    group_message_index_name = group_message_index_name_pre + current_date

    query_body = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'speaker_qq_number':qq_number}},
                    {'term':{'xnr_qq_number':qq_number}}
                ]
            }
        }
    }

    count_result = es.count(index=group_message_index_name,doc_type=group_message_index_type,body=query_body)

    if count_result['_shards']['successful'] != 0:
        today_count = count_result['count']
    else:
        print 'es index rank error'
        today_count = 0

    _id_last = xnr_user_no +'_'+ last_date
    print '_id_last::',_id_last

    try:
        get_result = es.get(index=qq_xnr_history_count_index_name,doc_type=qq_xnr_history_count_index_type,\
                            id=_id_last)['_source']
        total_count_history = get_result['total_post_num']
    except:
        total_count_history = 0

    total_count_totay = total_count_history + today_count

    _id_today = xnr_user_no + '_' + current_date

    item_dict = dict()
    item_dict['date_time'] = current_date
    item_dict['xnr_user_no'] = xnr_user_no
    item_dict['total_post_num'] = total_count_totay
    item_dict['daily_post_num'] = today_count
    item_dict['qq_number'] = qq_number
    item_dict['timestamp'] = timestamp
    print 'item_dict::',item_dict
    es.index(index=qq_xnr_history_count_index_name,doc_type=qq_xnr_history_count_index_type,\
                id=_id_today,body=item_dict)

def main_qq_count():
    query_body = {
        'query':{
            'match_all':{}
        },
        'size':MAX_VALUE
    }
    results = es.search(index=qq_xnr_index_name,doc_type=qq_xnr_index_type,body=query_body)['hits']['hits']

    for item in results:
        item = item['_source']
        xnr_user_no = item['xnr_user_no']
        qq_number = item['qq_number']
        current_time = time.time() - DAY
        qq_history_count(xnr_user_no,qq_number,current_time)

if __name__ == '__main__':

    # xnr_user_no = 'QXNR0001'
    # qq_number = '1965056593'
    # current_time = time.time()
    # qq_history_count(xnr_user_no,qq_number,current_time)

    main_qq_count()








