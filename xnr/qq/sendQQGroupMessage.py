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
from global_utils import es_xnr as es
from global_utils import group_message_index_name_pre, group_message_index_type, sent_group_message_index_name_pre
from qq_xnr_groupmessage_mappings import group_message_mappings
# es = Elasticsearch("http://219.224.134.213:9205/")

def sendfromweb(group,content):
    
    try:
        result = sendMessage(bot,group,content)
    except:
        bot.Login()
        result = sendMessage(bot,group,content)
    return result

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