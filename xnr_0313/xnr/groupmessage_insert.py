# -*-coding:utf-8-*-
# using to insert group message data into es
import sys
import json
from elasticsearch import helpers
from elasticsearch.helpers import scan
from global_utils import es_xnr as es
from global_utils import group_message_index_name_pre, group_message_index_type

from global_config import QQ_S_DATE

# 数据读入部分
f = open("qqbot.txt","r")
data = f.readlines()
# print(data)
messages = []
for item in data:
    if  item.strip():
        messages.append(eval(item))

# 初始化部分
date = QQ_S_DATE
index_name = group_message_index_name_pre + date
actions = []

# 数据插入循环
for message in messages:
    action ={
        "_index": index_name,
        "_type": group_message_index_type,
        "_id": str(message['xnr_qq_number'])+'_'+\
                str(message['qq_group_number'])+'_'+str(message['timestamp']),
        "_source": {
                       "qq_group_number":str(message['qq_group_number']),
                       "text":message['text'],
                       "speaker_qq_number":str(message['speaker_qq_number']),
                       "speaker_qq_nickname":str(message['speaker_nick']),
                       "xnr_qq_number":str(message['xnr_qq_number']),
                       "timestamp": str(message['timestamp'])
                       }
    }
    actions.append(action)
    if len(actions)==500000:
        helpers.bulk(es,actions)
        del actions[0:len(actions)]
# print actions
if len(actions) > 0:
    helpers.bulk(es, actions)
    print '插入成功%d条记录'%(len(actions))
    del actions[0:len(actions)]

# print message
f.close()