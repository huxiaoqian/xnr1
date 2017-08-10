# -*- coding: utf-8 -*-

# 如果不希望加载本插件，可以在配置文件中的 plugins 选项中删除 qqbot_test.plugins.grouplog
import datetime
import json

from qqbot import _bot as bot
from qqbot.utf8logger import INFO

from elasticsearch import Elasticsearch

es = Elasticsearch("http://219.224.134.213:9205/")
# from global_utils import es_xnr as es
# from global_utils import group_message_index_name, group_message_index_type


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
            qq_item = {
                'xnr_qq_number': bot.session.qq,
                'xnr_nickname': bot.session.nick,
                'timestamp': member.last_speak_time,
                'speaker_qq_number': member.qq,
                'text': content,
                'speaker_nickname': member.nick,
                'qq_group_number': contact.qq,
                'qq_group_nickname': contact.nick
            }
            qq_json = json.dumps(qq_item)
            print qq_json

            nowDate = datetime.datetime.now().strftime('%Y-%m-%d')
            index_name = 'group_message_' + str(nowDate)
            index_id = bot.conf.qq + '_' + contact.qq + '_' + str(member.last_speak_time)
            # es.index(index=index_name, doc_type='record', id=index_id, body=qq_item)


def execute():
    bot.Login()
    bot.Plug('receiveQQGroupMessage')
    bot.Run()


if __name__ == '__main__':
    execute()
