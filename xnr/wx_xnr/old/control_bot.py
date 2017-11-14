# -*- coding: utf-8 -*-
import socket
import json
import sys

def load_config():
    with open('wx_xnr_conf.json', 'r') as f:
        return json.load(f)

config = load_config()

def send_command(command):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((config['socket_host'], config['socket_port']))
        client.send(json.dumps(command))
        buf = []
        while True:
            d = client.recv(config['socket_buffer_size'])
            if d:
                buf.append(d)
            else:
                break
        data = ''.join(buf)
        if data:
            return json.loads(data)
        else:
            return None
    except Exception,e:
        print e
    finally:
        client.close()

def push_msg(ot_id, to_group_name, m):
    #通过输入名字，返回符合条件的群组，再经选择后使用push_msg_by_puid()发送消息
    msg = {'opt': 'pushmsg','bot_id': bot_id,'to_group_name': to_group_name, 'm': m}
    return send_command(msg)

def push_msg_by_puid(bot_id, to_group_puid, m):
    msg = {'opt': 'pushmsgbypuid','bot_id': bot_id,'to_group_puid': to_group_puid, 'm': m}
    return send_command(msg)

def load_groups(bot_id):
    command = {'opt': 'loadgroups', 'bot_id': bot_id}
    return send_command(command)

def load_group_members(bot_id, group_puid):
    command = {'opt': 'loadgroupmembers', 'bot_id': bot_id, 'group_puid': group_puid}
    return send_command(command)

def restart_bot(bot_id):
    command = {'opt': 'restartbot', 'bot_id': bot_id}
    return send_command(command)

if __name__ == '__main__':
    #opt: pushmsgbypuid loaduser loadgroupmembers loadgroups
    
    #test load_groups
    # for d in load_groups('bot_1'):
    #     print d[0], d[1]

    #test push_msg_by_puid
    # print push_msg_by_puid(bot_id='bot_1', to_group_puid='025abe43', m='测试一下')

    #test load_group_members
    # for d in  load_group_members(bot_id='bot_1', group_puid='1116ae91'):
    #     print d[0], d[1]

    #test restart_bot
    print restart_bot('bot_1')
    

