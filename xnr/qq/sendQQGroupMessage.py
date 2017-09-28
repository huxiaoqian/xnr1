# -*- coding: utf-8 -*-
import os
import subprocess

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

def sendfromweb(xnr_qq_number,group,content):
    # qq_port = '8188'
    qq_xnr_info = get_qqxnr_port(qq_xnr, group) 
    shell_str = 'qq '+qq_port+' send group '+ group + ' ' + content
    print 'shell_str:', shell_str
    p = subprocess.Popen(shell_str, \
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    line_list = ''
    for line in p.stdout.readlines():
        print 'return line:', line
        line_list += line
    '''
    try:
        result = sendMessage(bot,group,content)
    except:
        bot.Login()
        result = sendMessage(bot,group,content)
    '''
    if result:
        update_flag = speak_num_update(str(bot.session.qq))        #按照虚拟人qq号更新历史及当日发言信息
        # print bot.session.qq
        if update_flag:
            return 1    
    return 0
    

# 用于更新es中的历史和当日发言数
def speak_num_update(xnr_qq_number):
    today_num = compute_today_number(xnr_qq_number)
    history_num = compute_history_number(xnr_qq_number)
    # 将新数据存入数据库
    time.sleep(5)
    result = dataUpdate(xnr_qq_number,today_num,history_num)
    return result
    
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

def get_qqxnr_port(qq_xnr, group):
    qq_xnr_info = {}
    #step0: read qq_xnr es to get qqbot_port/xnr_qq_number/xnr_nickname
    #try:
        # qq_xnr_es_result = es.get(index_name=qq_xnr_index_name, doc_type=qq_xnr_index_type,\
        #         id=qq_xnr,_source=True)['_source']

    qq_xnr_search_result = es.search(index=qq_xnr_index_name, doc_type=qq_xnr_index_type,\
                 body={'query':{'term':{'qq_number':qq_xnr}}},_source=True)['hits']['hits']
    qq_xnr_es_result = qq_xnr_search_result[0]['_source']
    '''
    # except:
    #     print 'qq_xnr is not exist'
    #     return qq_xnr_info
    try:
        # qq_xnr_es_result = es.get(index_name=qq_xnr_index_name, doc_type=qq_xnr_index_type,\
        #         id=qq_xnr,_source=True)['_source']

        qq_xnr_search_result = es.search(index=qq_xnr_index_name, doc_type=qq_xnr_index_type,\
                     body={'query':{'term':{'qq_number':qq_number}}},_source=True)['hits']['hits']
        qq_xnr_es_result = qq_xnr_search_result[0]['_source']

    except:
        print 'qq_xnr is not exist'
        return qq_xnr_info
    '''
    #qqbot_port = '8189'
    qqbot_port = qq_xnr_es_result['qqbot_port']
    qq_xnr_info['qqbot_port'] = qqbot_port
    qq_xnr_info['xnr_qq_number'] = qq_xnr
    qq_xnr_info['xnr_nickname'] = qq_xnr_es_result['nickname']
    qq_xnr_info['speaker_qq_number'] = qq_xnr
    qq_xnr_info['speaker_nickname'] = qq_xnr_es_result['nickname']
    #step1: get qq_group_number
    print 'group::',group
    print 'group_type::',type(group)
    print 'qqbot_port_type::',type(qqbot_port)
    print 'qqbot_port::',qqbot_port

    p_str = 'qq '+ str(qqbot_port) + ' list group '+ group.encode('utf-8')
    p = subprocess.Popen(p_str, \
       shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    line_count = 0
    for line in p.stdout.readlines():
        line_count += 1
        if line_count == 5:
            item_line_list = line.split('|')
            qq_group_number = str(int(item_line_list[2]))
            #print 'item_line_list:', qq_group_number, len(qq_group_number)
    qq_xnr_info['qq_group_number'] = qq_group_number
    qq_xnr_info['qq_group_nickname'] = group

    print 'qq_xnr_info::',qq_xnr_info
    return qq_xnr_info

def sendfromweb_v2(qq_xnr, group, content):
    #step0: get qqbot port for qq_xnr
    qq_xnr_info = get_qqxnr_port(qq_xnr, group) 
    '''
    qq_xnr_info = {
    qqbot_port/xnr_qq_number/xnr_nickname/
    speaker_qq_number/speaker_nickname/qq_group_number/qq_group_nickname
    '''
    #step1: send message
    qqbot_port = qq_xnr_info['qqbot_port']
    #test
    #qqbot_port = '8199'
    shell_str = 'qq '+str(qqbot_port)+' send group '+ group.encode('utf-8') + ' ' + content.encode('utf-8')
    p = subprocess.Popen(shell_str, \
             shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #test
    line_list = ''
    for line in p.stdout.readlines():
       print 'return line:', line
       line_list += line
    
    if '成功' in line_list:
        qq_item = {
                   'xnr_qq_number': qq_xnr_info['xnr_qq_number'],
                   'xnr_nickname': qq_xnr_info['xnr_nickname'],
                   'timestamp': int(round(time.time())),
                   'speaker_qq_number': qq_xnr_info['speaker_qq_number'],
                   'text': content,
                   'speaker_nickname': qq_xnr_info['speaker_nickname'],
                   'qq_group_number': qq_xnr_info['qq_group_number'],
                   'qq_group_nickname': qq_xnr_info['qq_group_nickname']
                   }
        qq_json = json.dumps(qq_item)
        nowDate = datetime.datetime.now().strftime('%Y-%m-%d')
        index_name = sent_group_message_index_name_pre + str(nowDate)
        conMD5 = string_md5(content)
        index_id = qq_xnr_info['xnr_qq_number'] + '_' + qq_xnr_info['speaker_qq_number'] + '_' + str(int(round(time.time()))) + '_' + conMD5
        return 1
    else:
        return 0
    


if __name__ == '__main__':
    # bot.Login()
    # sendMessage(bot, 'SPDJ5', 'hi everyone')
    #sendfromweb('16美赛二群', 'o')
    # speak_num_update('365217204')
    sendfromweb_v2(qq_xnr, group, content)
