# -*-coding:utf-8-*-
import IP
import re
import csv
import sys
import zmq
import time
import json
import math
import redis
# from openpyxl import load_workbook
from elasticsearch import Elasticsearch
from datetime import datetime
# from triple_sentiment_classifier import triple_classifier
#from DFA_filter import createWordTree,searchWord 
from elasticsearch.helpers import scan
from global_utils_flow_text import black_words

sys.path.append('../')
from trans.trans import trans

reload(sys)
sys.path.append('../../')
from time_utils import ts2datetime,datetime2ts
from global_utils import R_CLUSTER_FLOW2 as r_cluster,twitter_flow_text_index_name_pre,\
                        twitter_flow_text_index_type,facebook_flow_text_index_name_pre,\
                        facebook_flow_text_index_type
from global_utils import es_xnr as es,R_UNAME2ID_FT, fb_uname2id, tw_uname2id
from global_utils import R_ADMIN as r_sensitive
from timed_python_files.twitter_mappings import twitter_flow_text_mappings
from parameter import sensitive_score_dict

fdf = open('diff_text_new2.txt','wb')

if __name__ == '__main__':

    #DFA = createWordTree()

    count = 0
    read_count = 0
    bulk_action = []
    action = []
    xdata = []
    tb = time.time()
    ts = tb
    index_name_pre = twitter_flow_text_index_name_pre
    index_type = twitter_flow_text_index_type
    start_date = '2017-10-24'
    end_date = '2017-10-24'

    start_ts = datetime2ts(start_date)
    end_ts = datetime2ts(end_date)

    days_num = (end_ts - start_ts)/(24*3600)+1

    count_diff = 0


    for i in range(days_num):
        current_time = start_ts + i*24*3600
        current_date = ts2datetime(current_time)
        index_name = index_name_pre + current_date
        print 'index......',index_name
        query_body = {
            'query':{
                'match_all':{}
            }
        }

        es_scan_results = scan(es,query=query_body,size=1000,index=index_name,\
            doc_type=index_type,scroll='30m')



        while 1:

            try:
                read_count += 1
                
                scan_data = es_scan_results.next()
                item = scan_data['_source']

                text = item['text']
                uid = item['uid']

                #try:
                text_ch = trans([text])[0]
                if text != text_ch:
                    count_diff += 1
                    #print 'text_ch....',text_ch
                    #print 'text.......',text
                    
                    fdf.write(text.encode('utf-8')+'\t'+text_ch.encode('utf-8'))
                    fdf.write('\n')

                # except:
                #     pass

            
                count += 1
                
                if count % 1000 == 0 and count != 0:
                    print count

                if count >= 500:
                    print 'count_diff..',count_diff
                    break

            except StopIteration:
                #print 'over!!!!'
                print 'count_diff.....',count_diff
                break

fdf.close()
