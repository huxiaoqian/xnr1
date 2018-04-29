#-*- coding:utf-8 -*-
'''
compute keywords
'''
import json
import time
import sys
reload(sys)
sys.path.append('../../')

from time_utils import ts2datetime,datetime2ts
from global_utils import es_xnr,weibo_keyword_count_index_name,weibo_keyword_count_index_type,\
                             xnr_flow_text_index_name_pre,xnr_flow_text_index_type,\
                             weibo_xnr_index_name,weibo_xnr_index_type,\
                             es_flow_text,flow_text_index_type, weibo_xnr_fans_followers_index_name,\
                             weibo_xnr_fans_followers_index_type, flow_text_index_name_pre, flow_text_index_type
from textrank4zh import TextRank4Keyword, TextRank4Sentence

test_date = '2016-11-27'

#实验流程，从flow_text_A取200个uid，去其中一个flow_text_B中做aggs聚合生成关键字测试时间
def extract_uidlist(fb_bcilist):
    query_body={
        'query':{
            'match_all':{}
        },
        'size':200,
        'sort':{'influence':{'order':'desc'}}
    }
    result=es_xnr.search(index=fb_bcilist,doc_type='bci',body=query_body)['hits']['hits']
    uid_list=[]
    for item in result:
        uid_list.append(item['_source']['uid'])
    return uid_list


def extract_keywords(w_text):

    tr4w = TextRank4Keyword()
    tr4w.analyze(text=w_text, lower=True, window=4)
    k_dict = tr4w.get_keywords(100, word_min_len=2)

    return k_dict



def xnr_keywords_compute(uid_list,fb_flow_textlist):
    lookup_condition_list=[]
    lookup_condition_list.append({'filtered':{'filter':{'bool':{'must':{'terms':{'uid':uid_list}}}}}})

    query_body={
        'query':lookup_condition_list[0],
        'aggs':{
            'keywords':{
                'terms':{
                    'field':'keywords_string',
                    'size': 1000
                }
            }
        }
    }
        
    flow_text_exist=es_xnr.search(index=fb_flow_textlist,doc_type=flow_text_index_type,\
           body=query_body)['aggregations']['keywords']['buckets']
    word_dict = dict()

    word_dict_new = dict()

    keywords_string = ''
    for item in flow_text_exist:
        word = item['key']
        count = item['doc_count']
        word_dict[word] = count

        keywords_string += '&'
        keywords_string += item['key']

    k_dict = extract_keywords(keywords_string)

    for item_item in k_dict:
        keyword = item_item.word
        # print 'keyword::',type(keyword)
        word_dict_new[keyword] = word_dict[keyword]
        

    return word_dict_new


if __name__ == '__main__':
    fb_bcilist=['fb_bci_2017-10-12','fb_bci_2017-10-13','fb_bci_2017-10-14','fb_bci_2017-10-15','fb_bci_2017-10-16','fb_bci_2017-10-17','fb_bci_2017-10-18']
    fb_flow_textlist=['facebook_flow_text_2017-10-12','facebook_flow_text_2017-10-13','facebook_flow_text_2017-10-14','facebook_flow_text_2017-10-15','facebook_flow_text_2017-10-19','facebook_flow_text_2017-10-20','facebook_flow_text_2017-10-21']
    uid_list=extract_uidlist(fb_bcilist)
    first_time=int(time.time())
    print 'first_time:',first_time
    result=xnr_keywords_compute(uid_list,fb_flow_textlist)
    print 'result:',result
    if result:
        secondtime=int(time.time())
        print 'secondtime:',secondtime
        print 'timecost:',secondtime - first_time