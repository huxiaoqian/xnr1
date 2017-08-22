# -*- coding: utf-8 -*-
import hashlib
import time
import json

import datetime
import types

from qqbot import _bot as bot
from elasticsearch import Elasticsearch

import sys
reload(sys)
sys.path.append('../')
from time_utils import datetime2ts, ts2datetime, get_groupmessage_index_list
from global_utils import es_xnr as es
from parameter import MAX_VALUE, DAY, group_message_windowsize
from global_utils import group_message_index_name_pre, group_message_index_type, sent_group_message_index_name_pre,\
                         qq_xnr_index_name,qq_xnr_index_type
from qq_xnr_groupmessage_mappings import group_message_mappings
# es = Elasticsearch("http://219.224.134.213:9205/")

def sendfromweb(group,content):
    
    try:
        result = sendMessage(bot,group,content)
    except:
        bot.Login()
        result = sendMessage(bot,group,content)
    if result:
        speak_num_update(str(bot.session.qq))        #按照虚拟人qq号更新历史及当日发言信息
        # print bot.session.qq
        
    return result

# 用于更新es中的历史和当日发言数
def speak_num_update(xnr_qq_number):
    today_num = compute_today_number(xnr_qq_number)
    history_num = compute_history_number(xnr_qq_number)
    # 将新数据存入数据库
    time.sleep(5)
    result = dataUpdate(xnr_qq_number,today_num,history_num)
    print result
    
def dataUpdate(xnr_qq_number,today_num,history_num):

    try:
        es.update(index=qq_xnr_index_name, doc_type=qq_xnr_index_type, id=xnr_qq_number,  body={"doc":{"today_speak_num":today_num, "all_speak_num": history_num}})
        return 1
    except:
        print '发言数更新失败'
        return 0
    

def compute_history_number(xnr_qq_number):
    query_body_history = {
        "query": {
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"term":{"xnr_qq_number":xnr_qq_number}}

                        ]
                    }
                }
            }
            },
            "size": MAX_VALUE,
            # "sort":{"timestamp":{"order":"desc"}}
        }


    enddate = datetime.datetime.now().strftime('%Y-%m-%d')
    startdate = ts2datetime(datetime2ts(enddate)-group_message_windowsize*DAY)
    index_names = get_groupmessage_index_list(startdate,enddate)
    print index_names
    results = {}
    for index_name in index_names:
        # if not es_xnr.indices.exsits(index=index_name):
        #     continue
        try:
            # 这里是把index名字改成发送表的名 sent_group_message_2017-07-07
            result = es.search(index='sent_'+index_name, doc_type=group_message_index_type,body=query_body_history)
            if results != {}:
                results['hits']['hits'].extend(result['hits']['hits'])
            else:
                results=result.copy()
        except:
            pass
    if results !={}:
        history_num = len(results['hits']['hits'])
    else:
        return 0
    return history_num




def compute_today_number(xnr_qq_number):
    nowDate = datetime.datetime.now().strftime('%Y-%m-%d')
    today_start_ts = datetime2ts(nowDate)
    today_end_ts = today_start_ts + DAY
    index_name = sent_group_message_index_name_pre + str(nowDate)
    query_body_today = {
        "query": {
            "filtered":{
                "filter":{
                    "bool":{
                        "must":[
                            {"term":{"xnr_qq_number":xnr_qq_number}}

                        ]
                    }
                }
            }
            },
            "size": MAX_VALUE,
            # "sort":{"timestamp":{"order":"desc"}}
        }


    today = es.search(index=index_name, doc_type=group_message_index_type, body=query_body_today)['hits']['hits']
    today_num = len(today)
    return today_num


def sendMessage(bot, group, content):
    bot.Update('group')
    gl = bot.List('group', group)
    print gl[0].qq
    if gl:
        qq_item = {
            'xnr_qq_number': bot.session.qq,
            'xnr_nickname': bot.session.nick,
            'timestamp': int(round(time.time())),
            'speaker_qq_number': bot.session.qq,
            'text': content,
            'speaker_nickname': bot.session.nick,
            'qq_group_number': gl[0].qq,
            'qq_group_nickname': group
        }
        qq_json = json.dumps(qq_item)
        print qq_json

        conMD5 = string_md5(content)

        nowDate = datetime.datetime.now().strftime('%Y-%m-%d')
        index_name = sent_group_message_index_name_pre + str(nowDate)
        index_id = bot.conf.qq + '_' + gl[0].qq + '_' + str(int(round(time.time()))) + '_' + conMD5
        # 将发送的信息存入es
        if not es.indices.exists(index=index_name):
            group_message_mappings(bot.session.qq,nowDate)

        es.index(index=index_name, doc_type=group_message_index_type, id=index_id, body=qq_item)

        bot.SendTo(gl[0], content)
        return 1
    else:
        print 'you no own this group', group
        return 0


def string_md5(str):
    md5 = ''
    if type(str) is types.StringType:
        _md5 = hashlib.md5()
        _md5.update(str)
        md5 = _md5.hexdigest()
    return md5


if __name__ == '__main__':
    # bot.Login()
    # sendMessage(bot, 'SPDJ5', 'hi everyone')
    sendfromweb('16美赛二群', 'o')
    # speak_num_update('365217204')