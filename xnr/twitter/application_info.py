#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys
sys.path.append('../')
from global_utils import es_xnr,tw_xnr_index_name,tw_xnr_index_type

def load_tw_app_api_info(xnr_user_no):
    results = es_xnr.get(index=tw_xnr_index_name,doc_type=tw_xnr_index_type,id=xnr_user_no)
    try:
        res = results['_source']
        info = {
            'access_secret': res['access_secret'],
            'access_token': res['access_token'],
            'consumer_key': res['consumer_key'],
            'consumer_secret': res['consumer_secret'],
        }
        return info
    except Exception,e:
        print e
        return False


'''
info = {
    'access_secret': access_secret,
    'access_token': access_token,
    'consumer_key': consumer_key,
    'consumer_secret': consumer_secret,
}
'''
def save_tw_app_api_info(xnr_user_no, info):
    try:
        if es_xnr.exists(index=tw_xnr_index_name, doc_type=tw_xnr_index_type, id=xnr_user_no):
            print es_xnr.update(index=tw_xnr_index_name, doc_type=tw_xnr_index_type, body={'doc': info}, id=xnr_user_no)
        else:
            print es_xnr.index(index=tw_xnr_index_name, doc_type=tw_xnr_index_type, id=xnr_user_no, body=info)
        return True
    except Exception,e:
        print e
        return False





if __name__ == '__main__':
    # print load_tw_app_api_info('TXNR0001')
    

    info = {
        'access_secret': 'KqNwtbK79hK95l4X37z9tIswNZSr6HKMSchEsPZ8eMxA9',
        'access_token': '943290911039029250-yWtATgV0BLE6E42PknyCH5lQLB7i4lr',
        'consumer_key': 'N1Z4pYYHqwcy9JI0N8quoxIc1',
        'consumer_secret': 'VKzMcdUEq74K7nugSSuZBHMWt8dzQqSLNcmDmpGXGdkH6rt7j2',
    }
    print save_tw_app_api_info('TXNR0001', info)