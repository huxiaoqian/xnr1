#-*-coding:utf-8-*-
import os
import json
import time
import random
import sys
sys.path.append('../')
from global_utils import es_xnr as es, fb_bci_index_name_pre, fb_bci_index_type,\
                        tw_bci_index_name_pre, tw_bci_index_type
from fb_tw_bci_mappings import tw_bci_mappings, fb_bci_mappings
from time_utils import datetime2ts, ts2datetime





#FXNR0005
fb_xnr_uid = '100018797745111'
#TXNR0003
tw_xnr_uid = '747226658457927680'






'''
Tools function
'''




'''
用于添加facebook_bci中xnr的数据
uid: 虚拟人uid
date: '2017-10-15'
'''
def create_facebook_bci_data(uid, date):
    fb_bci_index_name = fb_bci_index_name_pre + date
    fb_bci_mappings(fb_bci_index_name)
    data = {
        'active': random.choice([0,0,0,0,0,1,2]),
        'propagate': random.choice([3,6,12,18,3,6]),
        'cover': random.choice([1,1,1,1,1,1,1,1,1,2]),
        'trust': random.choice([0,0,0,0,0,0,0,0,0,0,1]),
        'influence': random.choice([4.771212547196624,7.781512503836437,10.79181246047625,14.471580313422193,]),
        'uid': uid,
        'timestamp': datetime2ts(date), 
    }
    print es.index(index=fb_bci_index_name,doc_type=fb_bci_index_type,id=uid,body=data)

'''
用于添加twitter_bci中xnr的数据
uid: 虚拟人uid
date: '2017-10-15'
'''
def create_twitter_bci_data(uid, date):
    tw_bci_index_name = tw_bci_index_name_pre + date
    tw_bci_mappings(tw_bci_index_name)
    data = {
        'active': random.choice([1,1,1,1,1,2,3]),
        'propagate': random.choice([1,1,1,1,1,1]),
        'cover': random.choice([1,1,1,1,12,18,31,43,90,201]),
        'trust': random.choice([0,0,0,0,0,0,0,0,0,0,0]),
        'influence': random.choice([10,10,20,12]),
        'uid': uid,
        'timestamp': datetime2ts(date), 
    }
    print es.index(index=tw_bci_index_name,doc_type=tw_bci_index_type,id=uid,body=data)

if __name__ == '__main__': 
    #2017-10-15  2017-10-25

    for i in range(15, 26, 1):
        date = '2017-10-' + str(i)
        print date
        # create_facebook_bci_data(fb_xnr_uid, date)
        create_twitter_bci_data(tw_xnr_uid, date)
