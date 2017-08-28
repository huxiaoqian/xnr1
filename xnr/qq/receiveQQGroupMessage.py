# -*- coding: utf-8 -*-

# 如果不希望加载本插件，可以在配置文件中的 plugins 选项中删除 qqbot_test.plugins.grouplog
import datetime
import hashlib
import json
import time
import types

from qqbot import _bot as bot
from qqbot.utf8logger import INFO

from elasticsearch import Elasticsearch

import sys, getopt
reload(sys)
sys.path.append('../')
sys.path.append('../cron/qq_group_message/')

# es = Elasticsearch("http://219.224.134.213:9205/")
from global_utils import es_xnr as es
from global_utils import group_message_index_name_pre, \
        group_message_index_type, qq_document_task_name

from qq_xnr_groupmessage_mappings import group_message_mappings
from sensitive_compute import sensitive_check


def onQQMessage(bot, contact, member, content):
    # 当收到 QQ 消息时被调用
    # bot     : QQBot 对象，提供 List/SendTo/GroupXXX/Stop/Restart 等接口，详见文档第五节
    # contact : QContact 对象，消息的发送者
    # member  : QContact 对象，仅当本消息为 群或讨论组 消息时有效，代表实际发消息的成员
    # content : str 对象，消息内容
    INFO('test groups %s', bot.List('group'))
    INFO('bot.conf %s', bot.conf)

    if contact.ctype == 'group':
        INFO('群的 QQ.. %s', contact.qq)
        INFO('群的昵称.. %s', contact.nick)
        INFO('成员的 QQ.. %s', member.qq)
        INFO('成员的昵称.. %s', member.nick)
        INFO('最后发言时间.. %s', member.last_speak_time)
        INFO('消息.. %s', content)

        if content == '':
            INFO('您发了一张图片或假消息... %s', content)
        else:
            sen_value,sen_words = sensitive_check(content)      # sen_words包含sensitive_words_string：北京&达赖和sensitive_words_dict
            if sen_value !=0:
                sen_flag = 1    #该条信息是敏感信息
            else:
                sen_flag = 0
            qq_item = {
                'xnr_qq_number': bot.session.qq,
                'xnr_nickname': bot.session.nick,
                'timestamp': member.last_speak_time,
                'speaker_qq_number': member.qq,
                'text': content,
                'sensitive_flag':sen_flag,
                'sensitive_value': sen_value,
                'sensitive_words_string': sen_words['sensitive_words_string'],
                'speaker_nickname': member.nick,
                'qq_group_number': contact.qq,
                'qq_group_nickname': contact.nick
            }
            qq_json = json.dumps(qq_item)
            print 'qq_json:',qq_json

            conMD5 = string_md5(content)
            '''
            nowDate = datetime.datetime.now().strftime('%Y-%m-%d')
            index_name = group_message_index_name_pre+ str(nowDate)
            index_id = bot.conf.qq + '_' + contact.qq + '_' + str(member.last_speak_time) + '_' + conMD5
            if not es.indices.exists(index=index_name):
                group_message_mappings(bot.session.qq,nowDate)

            es.index(index=index_name, doc_type=group_message_index_type, id=index_id, body=qq_item)
            '''

def string_md5(str):
    md5 = ''
    if type(str) is types.StringType:
        _md5 = hashlib.md5()
        _md5.update(str)
        md5 = _md5.hexdigest()
    return md5


def execute():
    bot.Login()
    bot.Plug('receiveQQGroupMessage')
    bot.Run()


def execute_v2(qqbot_port):
    bot.Login(['-p', qqbot_port])
    bot.Plug('receiveQQGroupMessage')
    bot.Run()

if __name__ == '__main__':
    #execute()
    opts, args = getopt.getopt(sys.argv[1:], 'hi:o:')
    for op, value in opts:
        if op == '-i':
            qqbot_port = value
            execute_v2(qqbot_port)
