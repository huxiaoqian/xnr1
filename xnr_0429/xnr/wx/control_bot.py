# -*- coding: utf-8 -*-
import os
import time
import socket
import json
import subprocess
from multiprocessing import Process
from MyWXBot import MyBot
import sys
sys.path.append(os.getcwd())
path1 = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir))
sys.path.append(path1)

from global_utils import es_xnr, wx_xnr_index_name, wx_xnr_index_type, wx_xnr_history_count_index_name, \
                        wx_xnr_history_count_index_type, wx_group_message_index_name_pre, wx_group_message_index_type, \
                        r_wx as r, WX_LOGIN_PATH, wx_xnr_data_path, wx_xnr_max_no,\
                        r as global_utils_r
global_utils_r = r #本来这个应该用默认的redis而不是微信的redis，但是默认的redis出现了点问题，先用微信的redis替代                      
es = es_xnr
from global_config import port_range
from parameter import MAX_VALUE, LOCALHOST_IP, DAY
from wx_xnr_manage_mappings import wx_xnr_mappings
from utils import user_no2wxbot_id, wxbot_id2user_no
from time_utils import ts2datetime, datetime2ts
from send_mail import send_mail

def IsOpen(ip,port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        result = s.connect_ex((ip,int(port)))
        if result:              #端口可用
            return True
        else:
            return False
    except:
        return False

def get_all_ports():
    query_body = {
        "query":{
            "match_all": {}
        },
        "size": MAX_VALUE
    }
    try:
        result = es_xnr.search(index=wx_xnr_index_name, doc_type=wx_xnr_index_type,body=query_body)['hits']['hits']
    except:
        return []
    results = []
    if result != []:
        for item in result:
            if item['_source']['wxbot_port'] not in results:
                results.append(int(item['_source']['wxbot_port']))
    return results

def find_port(exist_port_list):
    min_port = port_range[0]
    max_port = port_range[1]
    for port in range(min_port, max_port+1):
        if not port in exist_port_list:
            if IsOpen(LOCALHOST_IP,port):   #端口可用
                return port
    return False

def load_wxxnr_redis_data(wxbot_id, items=[]):
    d = r.get(wxbot_id)
    data = {}
    results = {}
    if d:
        data = eval(d)
        if items :
            for item in items:
                if item in data:
                    results[item] = data[item]
                else:
                    return 0
            return results
        else:
            return data
    else:
        return data

def change_wxxnr_redis_data(wxbot_id, xnr_data={}):
    d = r.get(wxbot_id)
    data = {}
    if d:
        data = eval(d)
    for key,value in xnr_data.items():
        data[key] = value   #如果存在key则更改数据为value,不存在key则增加数据value
    return r.set(wxbot_id, data)

''' 
#弃用，2018-4-27 12:11:40。使用get_wx_xnr_no()函数。    
def load_user_no_current():
    #返回将要新创建的wxbot的user_no
    query_body = {
      'query': {
        'match_all': {}
      },
      'sort': {
        'user_no': {
          'order': 'desc'
        }
      }
    }
    es_results = es_xnr.search(index=wx_xnr_index_name,doc_type=wx_xnr_index_type,body=query_body)['hits']['hits']
    if es_results:
        user_no_current = es_results[0]['_source']['user_no'] + 1 
    else:
        user_no_current = 1 
    return user_no_current
'''

#返回将要新创建的wxbot的user_no
def get_wx_xnr_no():
    user_no_max = 0
    if not global_utils_r.exists(wx_xnr_max_no): #如果当前redis没有记录，则去es数据库查找补上
        es_results = es.search(index=wx_xnr_index_name,doc_type=wx_xnr_index_type,body={'query':{'match_all':{}},\
                    'sort':{'user_no':{'order':'desc'}}})['hits']['hits']
        if es_results:
            user_no_max = es_results[0]['_source']['user_no']
    else:   #如果当前redis有记录，则取用
        user_no_max = int(global_utils_r.get(wx_xnr_max_no))
    return user_no_max


def check_wx_xnr(wx_id):
    wx_xnr_mappings()   #创建wx_xnr表
    query_body_wx_exist={'query':{'term':{'wx_id':wx_id}}}
    search_result = es_xnr.search(index=wx_xnr_index_name,doc_type=wx_xnr_index_type, body=query_body_wx_exist)['hits']['hits']
    
    if search_result:
        wxxnr_data = search_result[0]['_source']
        wxbot_id = wxxnr_data['xnr_user_no']
        wxbot_port = wxxnr_data['wxbot_port']
        wx_groups_puid = wxxnr_data.get('wx_groups_puid')
        if wx_groups_puid:
            groups_list = ','.join(wx_groups_puid)
        else:
            groups_list = ''
        data = {'wxbot_id':wxbot_id, 'wxbot_port':wxbot_port, 'groups_list':groups_list}
        return data
    return False

def login_wx_xnr(wxbot_id):
    try:
        wx_id = eval(r.get(wxbot_id))['wx_id']
        check_result = check_wx_xnr(wx_id)
        
        if check_result:
            wxbot_id = check_result['wxbot_id']
            wxbot_port = check_result['wxbot_port']
            groups_list = check_result['groups_list']
            qr_path = start_bot(wx_id=wx_id, wxbot_id=wxbot_id, wxbot_port=wxbot_port, init_groups_list=groups_list)
            return qr_path
    except Exception,e:
        print 'login_wx_xnr Exception: ',str(e)
        return 0

def create_wx_xnr(xnr_info):
    #create and login, xnr_info = [wx_id,remark,submitter,access_id]
    wx_id = xnr_info['wx_id']
    submitter = xnr_info['submitter']
    mail = xnr_info['mail']
    access_id = xnr_info['access_id']
    remark = xnr_info.get('remark')
    search_result = check_wx_xnr(wx_id) #check if wxxnr exist
    if search_result:   #如果虚拟人已经存在，则进行登陆。并可考虑用于更新wxxnr的信息，先不管
        wxbot_id = search_result['wxbot_id']
        wxbot_port = search_result['wxbot_port']
        groups_list = search_result['groups_list']
        #可进一步做出判断，如果wxbot_port被占用了，则更改wxbot_port，并更新es表。也先不管。
        qr_path = start_bot(wx_id=wx_id, wxbot_id=wxbot_id, wxbot_port=wxbot_port, init_groups_list=groups_list, submitter=submitter, mail=mail, access_id=access_id, remark=remark)
    else:   #如果虚拟人还没有存在，那么就创建此虚拟人
        wxbot_port = find_port(get_all_ports())
        
        # user_no_current = load_user_no_current()
        user_no_max = get_wx_xnr_no()
        user_no_current = user_no_max + 1
        global_utils_r.set(wx_xnr_max_no, user_no_current)

        wxbot_id = user_no2wxbot_id(user_no_current)
        qr_path = start_bot(wx_id=wx_id, wxbot_id=wxbot_id, wxbot_port=wxbot_port, submitter=submitter, mail=mail, access_id=access_id, remark=remark, create_flag=1)
    return qr_path

def start_bot(wx_id, wxbot_id, wxbot_port, submitter=None, mail=None, access_id=None, remark=None, init_groups_list='', create_flag=0):
    #在logout完善之前，在登录之前先手动把status数据更改成logout，并执行logout
    change_wxxnr_redis_data(wxbot_id, xnr_data={'status': 'logout','qr_path':'', 'wx_id':wx_id, 'wxbot_port':wxbot_port})

    #测试一下端口是否可用，不可用的话就更换端口
    if IsOpen(LOCALHOST_IP,wxbot_port):   #端口可用
        print 'wxbot_port ok', wxbot_port
        pass
    else:
        wxbot_port = find_port(get_all_ports())
        change_wxxnr_redis_data(wxbot_id, xnr_data={'wxbot_port':wxbot_port})
        data = {'wxbot_port':wxbot_port}
        es.update(index=wx_xnr_index_name, doc_type=wx_xnr_index_type, body={'doc': data}, id=wxbot_id)
        print 'new wxbot_port:', wxbot_port

    if submitter != None:
        change_wxxnr_redis_data(wxbot_id, xnr_data={'submitter':submitter})
    if mail != None:
        change_wxxnr_redis_data(wxbot_id, xnr_data={'mail':mail})
    if access_id != None:
        change_wxxnr_redis_data(wxbot_id, xnr_data={'access_id':access_id})
    if remark != None:
        change_wxxnr_redis_data(wxbot_id, xnr_data={'remark':remark})
    if create_flag:
        change_wxxnr_redis_data(wxbot_id, xnr_data={'create_flag':create_flag})
    logout_result = xnr_logout(wxbot_id)
    if logout_result:
        print u'登录前登出成功'
    else:
        print u'登录前登出失败'

    #login
    path2 = os.path.dirname(path1)
    wxxnr_login_path = os.path.join(path2, WX_LOGIN_PATH)
    print 'wxxnr_login_path: ', wxxnr_login_path
    if init_groups_list:
        base_str = 'python '+ wxxnr_login_path + ' -i '+ wxbot_id + ' -p ' + str(wxbot_port) +  ' -g ' + init_groups_list
    else:
        base_str = 'python '+ wxxnr_login_path + ' -i '+ wxbot_id + ' -p ' + str(wxbot_port)
   
    p_str1 = base_str + ' >> wxxnr_login'+ str(wxbot_port) + '.txt'
    #p_str1 = base_str
    
    print 'p_str1', p_str1


    command_str = base_str
    p_str2 = 'pgrep -f ' + '"' + command_str + '"'
    process_ids = subprocess.Popen(p_str2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    process_id_list = process_ids.stdout.readlines()
    for process_id in process_id_list:
        process_id = process_id.strip()
        kill_str = 'kill -9 ' + process_id
        p2 = subprocess.Popen(kill_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p2 = subprocess.Popen(p_str1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print 11111111
    '''
    #如果确定没错误，就注释掉这个
    for line in p2.stdout.readlines():
        print 'line: ', line
    ''' 
    print 222
    #检测登陆状态，返回登陆所需二维码路径或者返回缓存登录成功的标志：loginedwithcache
    while True:
        d = r.get(wxbot_id)
        if d:
            try:
                qr_path = eval(d)['qr_path']
                if qr_path:
                    print 'qr_path', qr_path
                #使用缓存登陆时，qr_path对应的二维码文件不存在
                if qr_path == 'loginedwithcache':
                    return qr_path
                if ('.png' in qr_path) and (os.path.isfile(qr_path)):
                    #发送二维码图片至邮箱
                    print 'start send mail ...'
                    if send_qrcode2mail(wxbot_id, qr_path):
                        print 'send mail SUCCESS'
                    else:
                        print 'send mail FAIL'
                    return qr_path
            except Exception,e:
                print e
                return 0

def send_command(command):
    wxbot_id = command['wxbot_id']
    wxbot_port = eval(r.get(wxbot_id))['wxbot_port']    #查询redis得到该wxbot_id对应的wxbot_port
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((LOCALHOST_IP, wxbot_port))
        client.send(json.dumps(command))
        buf = []
        while True:
            d = client.recv(8192)
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

def send_command_without_recv(command):
    wxbot_id = command['wxbot_id']
    wxbot_port = eval(r.get(wxbot_id))['wxbot_port']    #查询redis得到该wxbot_id对应的wxbot_port
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((LOCALHOST_IP, wxbot_port))
        client.send(json.dumps(command))
        result = 1
    except Exception,e:
        print 'send_command_without_recv Exception: ', str(e)
        result = 0
    finally:
        client.close()
    return result

def load_all_groups(wxbot_id):
    command = {'opt': 'loadallgroups', 'wxbot_id': wxbot_id}
    return send_command(command)

def set_groups(wxbot_id, group_list):
    #注册监听群消息的函数, group_list是需要监听消息的群组的puid列表
    command = {'opt': 'setgroups', 'wxbot_id': wxbot_id, 'group_list':group_list}
    return send_command(command)

def xnr_logout(wxbot_id):
    #无论监听群消息的端口开着与否都要保证执行完logout后是关闭状态
    command = {'opt': 'logout', 'wxbot_id': wxbot_id}
    result = send_command_without_recv(command)
    print 'xnr_logout test_send_resutl:'
    print result
    start_time = time.time()
    if not result:  #说明端口没有打开，只需要更改状态就行了
        if change_wxxnr_redis_data(wxbot_id, xnr_data={'status': 'logout'}):
            return 1 
    while True:
        end_time = time.time()
        d = r.get(wxbot_id)
        if d:
            status = eval(d)['status']
            if (status == 'logout') and result:
                #再执行一次，让server端执行server.close()的代码
                result = send_command_without_recv(command)
                if result:
                    return 1
                    break
        if int(end_time - start_time) > 8:
            break
    return 0

def check_status(wxbot_id):
    d = r.get(wxbot_id) 
    if d:
        try:
            status = eval(d)['status']
            if status == 'listening':
                #判断监听群组消息的socket端口是否在开着
                command = {'opt': 'checkstatus', 'wxbot_id': wxbot_id}
                if not send_command_without_recv(command):
                    status = 'logout'
                    change_wxxnr_redis_data(wxbot_id, {'status': status})
            return status
        except Exception,e:
            print e
    return 0

def show_wx_xnr():
    wx_xnr_mappings()   #创建wx_xnr表
    query_body={'query':{'match_all':{}},'size':MAX_VALUE}
    res = []
    res = es_xnr.search(index=wx_xnr_index_name, doc_type=wx_xnr_index_type, body=query_body)['hits']['hits']
    wx_xnr_list = []
    for item in res:
        data = item['_source']
        wxbot_id = data['xnr_user_no']
        xnr_data = {
            'wx_id': data['wx_id'],
            'wxbot_id': wxbot_id,
            'wxbot_port': data.get('wxbot_port'),
            'wx_groups_nickname': data.get('wx_groups_nickname'),
            'wx_groups_num': data.get('wx_groups_num'),
            'create_ts': data.get('create_ts'),
            'login_status': check_status(wxbot_id),
        }
        wx_xnr_list.append(xnr_data)
    return wx_xnr_list

def show_wx_xnr_listening_groups(wxbot_id):
    wx_xnr_mappings()   #创建wx_xnr表
    xnr_puid = load_wxxnr_redis_data(wxbot_id=wxbot_id, items=['puid'])['puid']
    query_body = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'puid':xnr_puid}}
                ]
            }
        }
    }
    res = []
    res = es_xnr.search(index=wx_xnr_index_name, doc_type=wx_xnr_index_type, body=query_body)['hits']['hits']
    wx_xnr_listening_groups = []
    for item in res:
        data = item['_source']
        wxbot_id = data['xnr_user_no']
        xnr_data = {
            'wxbot_id': wxbot_id,
            'wx_groups_nickname': data.get('wx_groups_nickname'),
            'wx_groups_id': data.get('wx_groups_puid')
        }
        wx_xnr_listening_groups.append(xnr_data)
    if len(wx_xnr_listening_groups) == 1:
        return wx_xnr_listening_groups[0]
    return 0
    
def delete_wx_xnr(wxbot_id):
    #是否要删除该wxbot捕获的群消息？
    try:
        #wx_xnr_logout
        xnr_logout(wxbot_id)
        #delete es data
        try:
            print es_xnr.delete(index=wx_xnr_index_name, doc_type=wx_xnr_index_type, id=wxbot_id)
        except Exception,e:
            print e
        #delete redis data
        r.delete(wxbot_id)
        #delete .pkl file
        cache_path = os.path.join(wx_xnr_data_path, wxbot_id + '.pkl')
        puid_path = os.path.join(wx_xnr_data_path, wxbot_id + '_puid.pkl')
        if os.path.isfile(cache_path):
            os.remove(cache_path)
            print 'remove :', cache_path
        if os.path.isfile(puid_path):
            os.remove(puid_path)
            print 'remove :', puid_path
        return 1
    except Exception,e:
        print e
        return 0

def send_msg(wxbot_id, puids, msg):
    #注册监听群消息的函数, group_list是需要监听消息的群组的puid列表
    command = {'opt': 'sendmsgbypuid', 'wxbot_id': wxbot_id, 'puids':puids, 'msg':msg}
    return send_command(command)

#目前仅支持qq邮箱
def send_qrcode2mail(wxbot_id, qr_path):
    try:
    	xnr_data = load_wxxnr_redis_data(wxbot_id=wxbot_id, items=['wx_id','nickname','mail','access_id'])
    	wx_id = xnr_data['wx_id']
    	nickname = xnr_data['nickname']
    	mail = xnr_data['mail']
    	password = xnr_data['access_id'] 
    	content = {
    	'subject': u'扫描二维码以登陆微信虚拟人',
    	'text': '请管理员及时扫码以登陆微信虚拟人【' + wx_id + '(' + nickname + ')' + '】，以免影响业务，谢谢。',
    	'files_path': qr_path,   #支持多个，以逗号隔开
    	}
    	from_user = {
            'name': u'虚拟人项目（微信）',
            'addr': mail,
            'password': password,   #其实应该是授权码
            'smtp_server': 'smtp.qq.com'   
    	}
    	to_user = {
            'name': u'管理员',
            'addr': mail  #支持多个，以逗号隔开
    	}	
        return send_mail(from_user=from_user, to_user=to_user, content=content)
    except Exception,e:
        print 'send_qrcode2mail Exception: ', str(e)
        return 0




