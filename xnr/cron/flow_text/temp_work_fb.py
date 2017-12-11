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
from openpyxl import load_workbook
from elasticsearch import Elasticsearch
from datetime import datetime
from triple_sentiment_classifier import triple_classifier
from DFA_filter import createWordTree,searchWord 
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


def uname2uid(uname,ft_type):
    uid = R_UNAME2ID_FT.hget(ft_type,uname)
    if not uid:
        #uid = uname
        return 0

    return uid

#for retweet message: get directed retweet uname and uid
#input: text, root_uid
#output: directed retweet uid and uname
def get_root_retweet(text, root_uid):
    # if isinstance(text, str):
    #     text = text.decode('utf-8', 'ignore')
    # RE = re.compile(u'Retweeted([a-zA-Z-_⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎 ]+)(@([a-zA-Z-_⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎 ]+)):', re.UNICODE)
    # repost_chains = RE.findall(text)
    # #print 'repost_chains...',repost_chains
    # if repost_chains != []:
    #     directed_uname = repost_chains[0]
    #     directed_uid = uname2uid(directed_uname)
    #     if not directed_uid:
    #         directed_uid = 0
    #         directed_uname = directed_uname
    # else:
    #     directed_uid = root_uid
    #     directed_uname = ''

    # return directed_uid, directed_uname
    if isinstance(text, str):
        text = text.decode('utf-8', 'ignore')

    if text.startswith('Retweeted '):
        #text = 'Retweeted iyouport (@iyouport_news): #AmericaChina 美国商务部周二表示'
        #RE = re.compile(u'Retweeted ([0-9a-zA-Z-_⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]+) ', re.UNICODE)
        #RE2 = re.compile(u' (@[0-9a-zA-Z-_⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]+):', re.UNICODE)
        RE2 = re.compile('.*@(.*)\).*', re.UNICODE)
        
        #repost_chains = RE.findall(text)
        repost_chains2 = RE2.findall(text)
        
        if repost_chains2 != []:
            root_uname = repost_chains2[0]
            root_uid = uname2uid(root_uname,ft_type=fb_uname2id)
    elif ' shared ' in text:
        res = text.split(' shared ')
        root_con = res[1]
        if "'s" in root_con:
            root_uname = root_con.split("'s")[0]
            root_uid = uname2uid(root_uname,ft_type=fb_uname2id)
        else:
            root_uname = ''
            root_uid = 0        
    else:
        root_uname = ''
        root_uid = 0

    return root_uid,root_uname


#use to expand index body to bulk action
#input: weibo_item
#output: action {'index':{'_id': mid}}, xdata {'mid':x, 'text':y,...}
def expand_index_action(item):
    index_body = {}
    index_body['uid'] = str(item['uid'])
    index_body['text'] = item['text']
    index_body['fid'] = str(item['fid'])
    index_body['sentiment'] = str(item['sentiment'])
    index_body['timestamp'] = int(item['timestamp'])
    #index_body['message_type'] = item['message_type']
    index_body['keywords_dict'] = item['keywords_dict']
    index_body['keywords_string'] = item['keywords_string']
    index_body['sensitive_words_string'] = item['sensitive_words_string']
    index_body['sensitive_words_dict'] = item['sensitive_words_dict']
    sensitive_words_dict = json.loads(item['sensitive_words_dict'])
    score = 0
    if sensitive_words_dict:
        #score = 0    
        for k,v in sensitive_words_dict.iteritems():
            tmp_stage = r_sensitive.hget("sensitive_words", k)
            if tmp_stage:
                score += v*sensitive_score_dict[str(tmp_stage)]
        #index_body['sensitive'] = score
    index_body['sensitive'] = score
        #print 'sensitive...index body...',index_body['sensitive']
    #if item['message_type'] == 3:

    #for retweet message: get directed retweet uname and uid 
    # directed_uid, directed_uname = get_directed_retweet(item['text'], item['root_uid'])
    directed_uid, directed_uname = get_root_retweet(item['text'], item['uid'])
    if directed_uid:
        index_body['directed_uid'] = long(directed_uid)
    else:
        #index_body['directed_uid'] = directed_uid
        index_body['directed_uid'] = 0

    index_body['directed_uname'] = directed_uname
    #index_body['root_fid'] = str(item['fid'])
    #index_body['root_uid'] = str(item['uid'])
    # elif item['message_type'] == 2:
    #     #for comment meesage: get directed comment uname and uid
    #     directed_uid, directed_uname = get_directed_comment(item['text'], item['root_uid'])
    #     if directed_uid:
    #         index_body['directed_uid'] = int(directed_uid)
    #     else:
    #         #index_body['directed_uid'] = directed_uid
    #         index_body['directed_uid'] = 0
    #     index_body['directed_uname'] = directed_uname
    #     index_body['root_fid'] = str(item['root_fid'])
    #     index_body['root_uid'] = str(item['root_uid'])

    # ip = item['send_ip']
    # index_body['ip'] = ip
    # index_body['geo'] = ip2city(ip) #output: 中国&河北&石家庄
    
    action = {'index': {'_id': index_body['fid']}}
    xdata = index_body
    #print 'index_body...',index_body
    return action, xdata


#get weibo keywords_dict and keywords_string
#write in version: 15-12-08
#input: keyowrds_list
#output: keywords_dict, keywords_string
def get_weibo_keywords(keywords_list):
    keywords_dict = {}
    keywords_string = ''
    filter_keywords_set = set()
    for word in keywords_list:
        if word not in black_words:
            try:
                keywords_dict[word] += 1
            except:
                keywords_dict[word] = 1
            filter_keywords_set.add(word)
    keywords_string = '&'.join(list(filter_keywords_set))

    return keywords_dict, keywords_string



if __name__ == '__main__':

    DFA = createWordTree()

    count = 0
    read_count = 0
    bulk_action = []
    action = []
    xdata = []
    tb = time.time()
    ts = tb
    index_name_pre = facebook_flow_text_index_name_pre
    index_type = facebook_flow_text_index_type
    start_date = '2017-09-10'
    end_date = '2017-10-25'
    # end_date = '2017-09-11'

    start_ts = datetime2ts(start_date)
    end_ts = datetime2ts(end_date)

    days_num = (end_ts - start_ts)/(24*3600)+1

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
            doc_type=index_type)

        while 1:
            try:
                read_count += 1
                
                scan_data = es_scan_results.next()
                item = scan_data['_source']

                text = item['text']
                uid = item['uid']
                
                try:
                    text_ch = trans([text])

                    if text_ch:
                        text = text_ch[0]
                        item['text'] = text_ch[0]
                except:
                    pass



                #add sentiment field to weibo
                sentiment, keywords_list  = triple_classifier(item)
                item['sentiment'] = str(sentiment)
                #add key words to weibo
                keywords_dict, keywords_string = get_weibo_keywords(keywords_list)
                item['keywords_dict'] = json.dumps(keywords_dict) # use to compute
                item['keywords_string'] = keywords_string         # use to search

                sensitive_words_dict = searchWord(text.encode('utf-8', 'ignore'), DFA)
                if sensitive_words_dict:
                    item['sensitive_words_string'] = "&".join(sensitive_words_dict.keys())
                    item['sensitive_words_dict'] = json.dumps(sensitive_words_dict)
                else:
                    item['sensitive_words_string'] = ""
                    item['sensitive_words_dict'] = json.dumps({})

                timestamp = item['timestamp']
                date = ts2datetime(timestamp)
                ts = datetime2ts(date)
                if sensitive_words_dict:
                    #print 'sensitive_words_dict...keys[0]...',sensitive_words_dict.keys()[0]
                    sensitive_count_string = r_cluster.hget('sensitive_'+str(ts), str(uid))
                    if sensitive_count_string: #redis取空
                        sensitive_count_dict = json.loads(sensitive_count_string)
                        for word in sensitive_words_dict.keys():
                            if sensitive_count_dict.has_key(word):
                                sensitive_count_dict[word] += sensitive_words_dict[word]
                            else:
                                sensitive_count_dict[word] = sensitive_words_dict[word]
                        r_cluster.hset('sensitive_'+str(ts), str(uid), json.dumps(sensitive_count_dict))
                    else:
                        r_cluster.hset('sensitive_'+str(ts), str(uid), json.dumps(sensitive_words_dict))

                #identify whether to mapping new es
                weibo_timestamp = item['timestamp']
                #should_index_name_date = ts2datetime(weibo_timestamp)
                # if should_index_name_date != now_index_name_date:
                if action != [] and xdata != []:
                    #index_name = index_name_pre + now_index_name_date
                    if bulk_action:
                        es.bulk(bulk_action, index=index_name, doc_type=index_type, timeout=60)
                    bulk_action = []
                    count = 0
                    # now_index_name_date = should_index_name_date
                    # index_name = index_name_pre + now_index_name_date
                    #twitter_flow_text_mappings(index_name)

                # save
                action, xdata = expand_index_action(item)
                bulk_action.extend([action, xdata])
                count += 1
                
                if count % 1000 == 0 and count != 0:
                    #index_name = index_name_pre + now_index_name_date
                    if bulk_action:
                        es.bulk(bulk_action, index=index_name, doc_type=index_type, timeout=60)
                    bulk_action = []
                    count = 0
                    class_te = time.time()
                    class_ts = class_te

                #run_type
                if read_count % 10000 == 0:
                    te = time.time()
                    print '[%s] cal speed: %s sec/per %s' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), te - ts, 10000) 
                    if read_count % 100000 == 0:
                        print '[%s] total cal %s, cost %s sec [avg %s per/sec]' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), read_count, te - tb, read_count / (te - tb)) 
                    ts = te

                # if read_count > 2:
                #     break

            except StopIteration:
                print 'over!!!!'
                break