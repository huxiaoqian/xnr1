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

def push_msg(m, bot_id='xb'):
    msg = {'opt': 'pushmsg','bot_id': bot_id, 'm': m}
    return send_command(msg)

def restart_bot(bot_id):
    command = {'opt': 'restartbot', 'bot_id': bot_id}
    return send_command(command)

if __name__ == '__main__':
    #opt: pushmsgbypuid
    #test push_msg_by_puid
    print push_msg(m='无聊', bot_id='xb')

    #test restart_bot
    # print restart_bot('bot_1')
    

