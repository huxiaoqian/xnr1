# -*- coding: utf-8 -*-
import hashlib
import time
import json

import datetime
import types

from qqbot import _bot as bot
from elasticsearch import Elasticsearch

es = Elasticsearch("http://219.224.134.213:9205/")

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
        index_name = 'group_message_' + str(nowDate)
        index_id = bot.conf.qq + '_' + gl[0].qq + '_' + str(int(round(time.time()))) + '_' + conMD5
        es.index(index=index_name, doc_type='record', id=index_id, body=qq_item)

        bot.SendTo(gl[0], content)
    else:
        print 'you no own this group', group


def string_md5(str):
    md5 = ''
    if type(str) is types.StringType:
        _md5 = hashlib.md5()
        _md5.update(str)
        md5 = _md5.hexdigest()
    return md5


if __name__ == '__main__':
    bot.Login()
    sendMessage(bot, 'SPDJ5', 'hi everyone')