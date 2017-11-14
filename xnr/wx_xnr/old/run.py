#-*- coding: utf-8 -*-
from wxpy import *
import os
import json
import random
import time
import socket
import threading
from multiprocessing import Process
from wx_xnr_es import WX_XNR_ES
from qiniu import Auth, put_file, etag, urlsafe_base64_encode

WX_XNR_Bot = {}
config = {}
qiniu = None
es_groupmsg = None

class MyBot(Bot):
    #继承Bot()，以便加入更多属性
    def __init__(self, bot_id, temp_path, data_path, es_groupmsg, if_enable_puid=None, if_cache_path=None, console_qr=False, qr_path=None, if_qr_callback=None, login_callback=None, logout_callback=None):
        self.bot_id = bot_id
        self.temp_path = temp_path
        self.data_path = data_path
        self.es_groupmsg = es_groupmsg
        self.if_enable_puid = if_enable_puid
        self.if_cache_path = if_cache_path
        self.console_qr = console_qr
        self.qr_path = qr_path
        self.if_qr_callback = if_qr_callback
        self.login_callback = login_callback
        self.logout_callback = logout_callback
        self.qr_callback = None

        self.logger = None  #负责将相关信息发送到微信监管群中
        
        if self.if_cache_path:
            self.cache_path = os.path.join(self.data_path, self.bot_id + '.pkl')
        if self.if_qr_callback:
            self.qr_path = os.path.join(self.temp_path, self.bot_id + '_qrcode.png')
            self.qr_callback = self.my_qr_callback
        #在控制台显示二维码进行登陆和将二维码图片保存到本地再使用其他方式进行扫描登陆只能选择其一
        if self.console_qr and self.if_qr_callback:
            print '控制台显示二维码和保存二维码图片只能选择其一'
            self.qr_path = None
            self.qr_callback = None

        #启动wxbot
        # try:
        #如果开启了缓存登陆，则先使用缓存登陆
        print '1111'
        Bot.__init__(self, self.cache_path, self.console_qr, self.qr_path, self.qr_callback, self.login_callback, self.logout_callback)
        print '2222'
        # except Exception,e :
        #     print '3333'
        #     print e
        #     os.remove(self.cache_path)
        #     #如果缓存登陆失败，则。。。。
        #     Bot.__init__(self, self.cache_path, self.console_qr, self.qr_path, self.qr_callback, self.login_callback, self.logout_callback)
        #     print '4444'
        #启用puid
        if self.if_enable_puid:
            self.enable_puid(os.path.join(self.data_path, self.bot_id + '_puid.pkl'))

        print self.self.puid

        @self.register(Group)
        def proc_group_msg(msg):
            self.save_msg(msg)
        
    def my_qr_callback(self, **kwargs):
        with open(self.qr_path, 'wb') as fp:
            fp.write(kwargs['qrcode'])
        #可以将二维码图片发送到邮箱之类的……

    def enable_logger(self, group_name):
        group_receiver = ensure_one(self.groups(update=True).search(group_name))
        self.logger = get_wechat_logger(group_receiver)

    def save_sent_msg(self, m, to_puid, to_name):
        data = {
            'msg_type': m.type,
            'text': m.text,
            'timestamp': int(time.mktime(m.create_time.timetuple())),
            'xnr_id': self.self.puid, 
            'xnr_name': self.self.name, 
            'group_id': to_puid, 
            'group_name': to_name,
            'speaker_id': self.self.puid, 
            'speaker_name': self.self.name
        }
        self.es_groupmsg.save_data(doc_type=self.es_groupmsg.doc_type, data=data)

    def save_msg(self, msg):
        d = {'xnr_id': self.self.puid, 'xnr_name': self.self.name, 'group_id': msg.sender.puid, 'group_name': msg.sender.name}
        if msg.type == 'Text':
            data = d
            data['msg_type'] = 'Text'
            data['text'] = msg.text
            data['timestamp'] = msg.raw['CreateTime']
            data['speaker_id'] = msg.member.puid
            data['speaker_name'] = msg.member.name
            self.es_groupmsg.save_data(doc_type=self.es_groupmsg.doc_type, data=data)  #保存群文本消息到es数据库中
        if msg.type == 'Picture':
            data = d
            data['msg_type'] = 'Picture'
            data['timestamp'] = msg.raw['CreateTime']
            data['speaker_id'] = msg.member.puid
            data['speaker_name'] = msg.member.name
            #save picture
            filename = str(msg.id) + '.png'
            filepath = os.path.join(self.temp_path, filename)
            msg.get_file(filepath)
            #upload picture to qiniu.com
            try:
                token = qiniu.upload_token(config['qiniu_bucket_name'], filename, 3600)
                ret, info = put_file(token, filename, filepath,)
                data['text'] = config['qiniu_bucket_domain'] + '/' + filename
                self.es_groupmsg.save_data(doc_type=self.es_groupmsg.doc_type, data=data)  
                os.remove(filepath)
            except Exception,e:
                print e
        #注册多个bot时，艾特功能不好使
        if msg.is_at:
            time.sleep(random.random())
            m = msg.reply(u'知道啦~')
            self.save_sent_msg(m=m, to_puid=msg.sender.puid, to_name=msg.sender.name)

def load_config():
    with open('wx_xnr_conf.json', 'r') as f:
        return json.load(f)

def init_es():
    es_groupmsg = WX_XNR_ES(host=config['es_host'], index_name=config['es_wx_xnr_groupmsg_index_name'], doc_type=config['es_wx_xnr_groupmsg_index_type'])
    es_groupmsg.create_index()
    es_groupmsg.put_mapping(doc_type=es_groupmsg.doc_type, mapping=config['wx_xnr_groupmsg_mapping'])
    return es_groupmsg

def load_groups(bot_id):
    bot = WX_XNR_Bot[bot_id]
    groups = bot.groups(update=True)
    data = []
    for group in groups:
        data.append((group.puid, group.name))
    return data

def load_group_members(bot_id, puid):
    bot = WX_XNR_Bot[bot_id]
    data = []
    for member in ensure_one(WX_XNR_Bot[bot_id].search(puid=puid)).members:
        data.append((member.puid, member.name))
    return data

def push_msg_by_puid(bot_id, puid, msg):
    try:
        bot = WX_XNR_Bot[bot_id]
        u = ensure_one(bot.search(puid=puid))
        m = u.send(msg)
        #save sent msg
        bot.save_sent_msg(m=m, to_puid=u.puid, to_name=u.name)
        return 'true'
    except Exception,e:
        print e
        return 'false'

def restart_bot(bot_id):
    try:
        bot = WX_XNR_Bot[bot_id]
        bot.logout()
    except:
        pass
    try:
        bot = MyBot(bot_id=bot_id, temp_path=config['temp_path'], data_path=config['data_path'], es_groupmsg=es_groupmsg, if_enable_puid=True, if_cache_path=True, console_qr=False, if_qr_callback=True)
        bot.enable_logger(u'微信虚拟人状况监管群')
        WX_XNR_Bot[bot_id] = bot
        return 'true'
    except Exception,e :
        print e
        return 'false'

def tcplink(conn, addr):
    print 'Accept new connection from %s:%s...'  % addr
    data = conn.recv(config['socket_buffer_size'])
    result = None
    if data:
        data = json.loads(data)
        opt = data['opt']
        if opt == 'loadgroups':
            result = load_groups(data['bot_id'])
        elif opt == 'pushmsgbypuid':
            result = push_msg_by_puid(bot_id=data['bot_id'], puid=data['to_group_puid'], msg=data['m'])
        elif opt == 'loadgroupmembers':
            result = load_group_members(bot_id=data['bot_id'], puid=data['group_puid'])
        elif opt == 'restartbot':
            result = restart_bot(bot_id=data['bot_id'])
        #发送结果给客户端
        conn.send(json.dumps(result))
    conn.close()  
    print 'Connection from %s:%s closed.' % addr
    
def control_bot():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((config['socket_host'], config['socket_port']))
    server.listen(5)    #等待连接的最大数量为5
    while True:
        conn, addr = server.accept()
        t = threading.Thread(target=tcplink, args=(conn, addr))
        t.start()
 
def main():
    global config
    global qiniu
    global es_groupmsg
    config = load_config()
    es_groupmsg = init_es()
    temp_path = config['temp_path']
    data_path = config['data_path']
    qiniu = Auth(config['qiniu_access_key'], config['qiniu_secret_key'])
    for i in range(config['bot_num']):
        bot_id = 'bot_' + str(i+1)
        print 'starting %s ...' % bot_id
        bot = MyBot(bot_id=bot_id, temp_path=temp_path, data_path=data_path, es_groupmsg=es_groupmsg, if_enable_puid=True, if_cache_path=True, console_qr=False, if_qr_callback=True)
        #使用微信群监管wxbot状况
        bot.enable_logger(u'微信虚拟人状况监管群')
        WX_XNR_Bot[bot_id] = bot
    #开启所有的wxbot之后，主进程监听有没有要主动发送消息的任务
    print 'ready to publish messages ...'
    control_bot() 

if __name__ == '__main__':
    main()