# -*- coding: utf-8 -*-
'''
use to save function---about deal database
'''
import time
import sys
import json
import subprocess
from xnr.global_utils import es_xnr,qq_xnr_index_name,\
        qq_xnr_index_type, ABS_LOGIN_PATH,QRCODE_PATH,r_qq_group_set_pre,r_qq_group_mark_set_pre,r, qq_xnr_max_no
from xnr.global_utils import qq_xnr_history_count_index_name,qq_xnr_history_count_index_type,\
                        group_message_index_name_pre,group_message_index_type
from xnr.parameter import MAX_VALUE,LOCALHOST_IP
from xnr.utils import user_no2qq_id
from xnr.time_utils import ts2datetime,datetime2ts
import socket
from xnr.qq.getgroup import getgroup_v2
from xnr.qq.receiveQQGroupMessage import execute_v2


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
        result = es_xnr.search(index=qq_xnr_index_name, doc_type=qq_xnr_index_type,body=query_body)['hits']['hits']
    except:
        return []
    results = []
    if result != []:
        for item in result:
            if item['_source']['qqbot_port'] not in results:
                results.append(int(item['_source']['qqbot_port']))
    return results

def find_port(exist_port_list):
    if exist_port_list != []:
        port = max(exist_port_list)
        port += 1
    else:
        port = 1025
    while port<=65535:
        if IsOpen(LOCALHOST_IP,port):
            break
        port +=1
    return port


def get_qq_xnr_no():
    
    if not r.exists(qq_xnr_max_no): #如果当前redis没有记录，则去es数据库查找补上
        user_no_max = 1
        r.set(qq_xnr_max_no,user_no_max)
    else:   #如果当前redis有记录，则取用
        user_no_max = r.incr(qq_xnr_max_no)

    return user_no_max

def create_qq_xnr(xnr_info):
# xnr_info = [qq_number,qq_groups,nickname,active_time,create_time]
    qq_group_exist_list = ''#[]
    qq_group_new_list = []
    qq_number = xnr_info['qq_number']
    #qq_groups = xnr_info['qq_groups'].encode('utf-8').split('，')
    group_names = xnr_info['group_names'].encode('utf-8').split('，')
    mark_names = xnr_info['mark_names'].encode('utf-8').split('，')
    group_numbers = xnr_info['group_numbers'].encode('utf-8').split('，')
    print 'group_numbers...',group_numbers
    if not len(group_names)==len(mark_names)==len(group_numbers):
        #return [False,'群名称数量和群号码数量不一致']
        return [False,'not_equal']

    if len(group_numbers) != 0:
        return [False, 'null']

    # redis 群名
    r_qq_group_set = r_qq_group_set_pre + qq_number

    mark_name_exist_list = []
    
    nickname = xnr_info['nickname']
    access_id = xnr_info['access_id']
    remark = xnr_info['remark']
    submitter = xnr_info['submitter']

    
    #r_qq_group_mark_set = r_qq_group_mark_set_pre + qq_number

    query_body_qq_exist = {
        'query':{
            'term':{'qq_number':qq_number}
        }
    }

    search_result = es_xnr.search(index=qq_xnr_index_name,doc_type=qq_xnr_index_type,\
        body=query_body_qq_exist)['hits']['hits']

    if search_result:
        #return ['当前qq已经被添加！',qq_group_exist_list]
        group_info = json.loads(search_result[0]['_source']['group_info'])
        group_info_keys = group_info.keys() # 群号

        for i in range(len(group_numbers)):

            group_qq_number = group_numbers[i]
            group_qq_name = group_names[i]
            group_qq_mark = mark_names[i]

            if group_qq_number in group_info_keys:   # 若群号已添加，则可修改群名
                #qq_group_exist_list.append(group_qq_number)
                #mark_name_list = group_info[group_qq_number]['mark_name']
                group_name_list = group_info[group_qq_number]['group_name']

                if not group_qq_name in group_name_list:
                    group_info[group_qq_number]['group_name'].append(group_qq_name)

            else:  # 若群号未添加，首先检查备注名是否重复，若重复，则返回，否则，正常流程。
                if not r.sadd(r_qq_group_set,group_qq_mark):  # 群号唯一 改为 备注唯一
                    mark_name_exist_list.append(group_qq_mark)
                else:
                    group_info[group_qq_number] = {'mark_name':group_qq_mark,'group_name':[group_qq_name]}

        if mark_name_exist_list:
            return [False,'失败！以下备注名重复：' + ','.join(mark_name_exist_list)]

        qqbot_port = search_result[0]['_source']['qqbot_port']
        
        # 把不在的群添加进去           
        qq_exist_result = search_result[0]['_source']
        xnr_user_no = qq_exist_result['xnr_user_no']
        qq_exist_result['group_info'] = json.dumps(group_info)

        qq_exist_result['qq_group_num'] = len(group_info)

        es_xnr.update(index=qq_xnr_index_name,doc_type=qq_xnr_index_type,id=xnr_user_no,\
            body={'doc':qq_exist_result})

        result = True
    else:

        # active_time = xnr_info[3]
        create_ts = xnr_info['create_ts']
        exist_port_list = get_all_ports()           #返回list形式int型端口号
        qqbot_port = find_port(exist_port_list)
        #qq_groups_num = len(qq_groups)
        # qq_groups = getgroup_v2(qq_number)
        user_no_current = get_qq_xnr_no()
        xnr_user_no = user_no2qq_id(user_no_current)  #五位数 QXNR0001
        
        # 群信息
        group_info = {}
        
        for i in range(len(group_numbers)):
            group_qq_number = group_numbers[i]
            group_qq_name = group_names[i]
            group_qq_mark = mark_names[i]

            if not r.sadd(r_qq_group_set,group_qq_mark):  # 群号唯一 改为 备注唯一. 存入redis,后面接收群消息时，用于过滤消息。
                mark_name_exist_list.append(group_qq_mark)
            else:
                group_info[group_qq_number] = {'mark_name':group_qq_mark,'group_name':[group_qq_name]}


        if mark_name_exist_list:
            return [False,'失败！以下备注名重复：' + ','.join(mark_name_exist_list)]

        qq_group_num = len(group_info)
        group_info = json.dumps(group_info)


        try:        
            ## 存入es
            es_xnr.index(index=qq_xnr_index_name, doc_type=qq_xnr_index_type, id=xnr_user_no, \
            body={'qq_number':qq_number,'nickname':nickname,'group_info':group_info,'qq_group_num':qq_group_num,'create_ts':create_ts,\
                    'qqbot_port':qqbot_port,'user_no':user_no_current,'xnr_user_no':xnr_user_no,\
                    'access_id':access_id,'remark':remark,'submitter':submitter})
            
            result = True
        except:
            result = False

    print 'before python recieveQQGroupMessage:', result

    if result == True:
        
        #qqbot_port = '8199'
        p_str1 = 'python '+ ABS_LOGIN_PATH + ' -i '+str(qqbot_port) + ' >> login'+str(qqbot_port)+'.txt'
        #qqbot_port = '8190'
        qqbot_num = qq_number
        qqbot_port = str(qqbot_port)
        qqbot_mc = access_id #'sirtgdmgwiivbegf'
        #qqbot_mc = 'worunhzbzyipdagc'
        p_str1 = 'python '+ ABS_LOGIN_PATH + ' -i '+qqbot_port + ' -o ' + qqbot_num + ' -m ' + qqbot_mc + ' >> login'+qqbot_port+'.txt'
        #p_str1 = 'python '+ ABS_LOGIN_PATH + ' -i '+qqbot_port + ' -o ' + qqbot_num + ' -m ' + qqbot_mc
        command_str = 'python '+ ABS_LOGIN_PATH + ' -i '+qqbot_port + ' -o ' + qqbot_num + ' -m ' + qqbot_mc
        print 'p_str1:', p_str1
        p_str2 = 'pgrep -f ' + '"' + command_str + '"'
        print 'p_str2::',p_str2
        process_ids = subprocess.Popen(p_str2, \
                shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        process_id_list = process_ids.stdout.readlines()
        
        for process_id in process_id_list:
            process_id = process_id.strip()
            kill_str = 'kill -9 ' + process_id
            print 'kill_str::',kill_str
            p2 = subprocess.Popen(kill_str, \
                shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        p2 = subprocess.Popen(p_str1, \
                shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        #print 'output:', p2.stdout.readlines()
        
    return [result,qq_group_exist_list]

def show_qq_xnr(MAX_VALUE):
    query_body = {
        'query':{
            'match_all':{}
        },
        'size':MAX_VALUE
    }
    results = []
    result = es_xnr.search(index=qq_xnr_index_name, doc_type=qq_xnr_index_type, body=query_body)['hits']['hits']
    qq_xnr_list = []
    for item in result:
        item_dict = dict()
        temp = item['_source'].copy()
        item_dict = dict(item_dict, **temp)
        #step1: identify login status
        port = item['_source']['qqbot_port']
        qqnum = item['_source']['qq_number']
        xnr_user_no = item['_source']['xnr_user_no']
        group_dict = getgroup_v2(xnr_user_no)
        #group_dict = True
        print 'hhhhh'
        print 'group_dict:::',group_dict
        if group_dict:
            login_status = True
        else:
            login_status = False
        item_dict['login_status'] = login_status
        now_date = ts2datetime(time.time() - 24*3600)
        histroy_id = item['_source']['xnr_user_no'] + '_' + now_date
        try:
            history_result = es_xnr.get(index=qq_xnr_history_count_index_name,\
                doc_type=qq_xnr_history_count_index_type, id=histroy_id)['_source']
            total_post_num = history_result['total_post_num']
            daily_post_num = history_result['daily_post_num']
        except:
            total_post_num = 0
            daily_post_num = 0
        # item_dict['total_post_num'] = total_post_num
        #item_dict['daily_post_num'] = daily_post_num

        
        group_message_index_name = group_message_index_name_pre + ts2datetime(time.time())

        query_body = {
            'query':{
                'bool':{
                    'must':[
                        {'term':{'speaker_qq_number':qqnum}},
                        {'term':{'xnr_qq_number':qqnum}}
                    ]
                }
            }
        }
        try:
            count_result = es_xnr.count(index=group_message_index_name,doc_type=group_message_index_type,body=query_body)

            if count_result['_shards']['successful'] != 0:
                today_count = count_result['count']
            else:
                print 'es index rank error'
                today_count = 0
        except:
            today_count = 0

        item_dict['daily_post_num'] = today_count
        item_dict['total_post_num'] = total_post_num + today_count
        results.append(item_dict)

    return results

def delete_qq_xnr(qq_number):
    try:
        es_xnr.delete(index=qq_xnr_index_name, doc_type=qq_xnr_index_type, id=qq_number)
        result = 1
    except:
        result = 0
    return result

def change_qq_xnr(xnr_user_no,group_names_string,group_numbers_string):

    get_result = es_xnr.get(index=qq_xnr_index_name,doc_type=qq_xnr_index_type,id=xnr_user_no)['_source']

    group_info = json.loads(get_result['group_info'])

    group_names = group_names_string.encode('utf-8').split('，')
    group_numbers = group_numbers_string.encode('utf-8').split('，')

    if len(group_numbers) != len(group_names) and len(group_numbers) != 0:
        return 'not_equal'

    group_numbers_origin = group_info.keys()

    delete_list = list(set(group_numbers_origin).difference(set(group_numbers)))
    #add_list = list(set(group_numbers).difference(set(group_numbers_origin)))

    if delete_list:
        for item in delete_list:
            group_info.pop(item)

    for i in range(len(group_numbers)):
        group_qq_number = group_numbers[i]
        group_qq_name = group_names[i]

        if group_qq_number not in group_numbers_origin:  # 新添加的
            group_info[group_qq_number] = [group_qq_name,'']
            r.sadd(r_qq_group_set,group_qq_number)  ## 存入redis,后面接收群消息时，用于过滤消息。

    qq_group_num = len(group_info)
    group_info = json.dumps(group_info)

    try:
        es_xnr.update(index=qq_xnr_index_name, doc_type=qq_xnr_index_type, id=xnr_user_no,  \
            body={"doc":{'group_info':group_info,'qq_group_num':qq_group_num}})
        result = True #'Successfully changed'
    except:
        result = False #'Changing Failed'

    return result

def search_qq_xnr(qq_number):
    query_body = {
    "query": {
        "filtered":{
            "filter":{
                "term":{"qq_number": qq_number}
            }
        }
    },
    'size':MAX_VALUE
}

    result = es_xnr.search(index=qq_xnr_index_name, doc_type=qq_xnr_index_type, body=query_body)
    
    return result



