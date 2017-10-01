# -*- coding: utf-8 -*-
'''
use to save function---about deal database
'''
import time
import sys
import subprocess
from xnr.global_utils import es_xnr,qq_xnr_index_name,\
        qq_xnr_index_type, ABS_LOGIN_PATH,QRCODE_PATH,r_qq_group_set_pre,r
from xnr.global_utils import qq_xnr_history_count_index_name,qq_xnr_history_count_index_type
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


def create_qq_xnr(xnr_info):
# xnr_info = [qq_number,qq_groups,nickname,active_time,create_time]
    qq_group_exist_list = []
    qq_group_new_list = []
    qq_number = xnr_info['qq_number']
    qq_groups = xnr_info['qq_groups'].encode('utf-8').split('，')
    #qqbot_mc = xnr_info['qqbot_mc']
    nickname = xnr_info['nickname']
    access_id = xnr_info['access_id']
    remark = xnr_info['remark']
    submitter = xnr_info['submitter']
    # redis 群名
    r_qq_group_set = r_qq_group_set_pre + qq_number

    query_body_qq_exist = {
        'query':{
            'term':{'qq_number':qq_number}
        }
    }

    search_result = es_xnr.search(index=qq_xnr_index_name,doc_type=qq_xnr_index_type,\
        body=query_body_qq_exist)['hits']['hits']

    if search_result:
        #return ['当前qq已经被添加！',qq_group_exist_list]
    
        for group_qq_number in qq_groups:
            query_body_qq_group_exist = {
                'query':{
                    'bool':{
                        'must':[
                            {'term':{'qq_number':qq_number}},
                            {'term':{'qq_groups':group_qq_number}}
                        ]
                    }
                }
            }

            exits_result = es_xnr.search(index=qq_xnr_index_name,doc_type=qq_xnr_index_type,\
            body=query_body_qq_group_exist)['hits']['hits']
            print 'exits_result::',exits_result
            if exits_result:
                qq_group_exist_list.append(group_qq_number)

            else:
                print '!!!!redis',r.sadd(r_qq_group_set,group_qq_number)
                qq_group_new_list.append(group_qq_number)
        qqbot_port = search_result[0]['_source']['qqbot_port']
        #if not qq_group_new_list:
        #    return ['当前群已经添加',qq_group_exist_list]
        result = True
        if qq_group_new_list:
            # 把不在的群添加进去
            qq_exist_results = es_xnr.search(index=qq_xnr_index_name,doc_type=\
                qq_xnr_index_type,body={'query':{'term':{'qq_number':qq_number}}})['hits']['hits']
            
            qq_exist_result = qq_exist_results[0]['_source']
            xnr_user_no = qq_exist_result['xnr_user_no']
            qq_groups = qq_exist_result['qq_groups']
            qq_groups.extend(qq_group_new_list)
            qq_exist_result['qq_groups'] = qq_groups
            qq_exist_result['qq_group_num'] = len(qq_groups)

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

        es_results = es_xnr.search(index=qq_xnr_index_name,doc_type=qq_xnr_index_type,body={'query':{'match_all':{}},\
                        'sort':{'user_no':{'order':'desc'}}})['hits']['hits']
        if es_results:
            user_no_max = es_results[0]['_source']['user_no']
            user_no_current = user_no_max + 1 
        else:
            user_no_current = 1

        #task_detail['user_no'] = user_no_current
        xnr_user_no = user_no2qq_id(user_no_current)  #五位数 QXNR0001
        print 'xnr_user_no:', xnr_user_no
        try:
            # if es_xnr.get(index=qq_xnr_index_name, doc_type=qq_xnr_index_type, id=qq_number):
            #     return 0
            
            ## 存入es
            es_xnr.index(index=qq_xnr_index_name, doc_type=qq_xnr_index_type, id=xnr_user_no, \
            body={'qq_number':qq_number,'nickname':nickname,'qq_groups':qq_groups,'qq_group_num':len(qq_groups),'create_ts':create_ts,\
                    'qqbot_port':qqbot_port,'user_no':user_no_current,'xnr_user_no':xnr_user_no,\
                    'access_id':access_id,'remark':remark,'submitter':submitter})
            
            ## 存入redis
            
            for qq_group_number in qq_groups:
                print '###redis',r.sadd(r_qq_group_set,qq_group_number)
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
        p_str1 = 'python '+ ABS_LOGIN_PATH + ' -i '+qqbot_port + ' -o ' + qqbot_num + ' -m ' + qqbot_mc + ' >> login'+qqbot_port+'.txt'
        #p_str1 = 'python '+ ABS_LOGIN_PATH + ' -i '+qqbot_port + ' -o ' + qqbot_num + ' -m ' + qqbot_mc
        print 'p_str1:', p_str1
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
        item_dict['total_post_num'] = total_post_num
        item_dict['daily_post_num'] = daily_post_num
        results.append(item_dict)

    return results

def delete_qq_xnr(qq_number):
    try:
        es_xnr.delete(index=qq_xnr_index_name, doc_type=qq_xnr_index_type, id=qq_number)
        result = 1
    except:
        result = 0
    return result

def change_qq_xnr(xnr_info):
    qq_number = xnr_info[0]
    qq_groups = xnr_info[1]
    try:
        es_xnr.update(index=qq_xnr_index_name, doc_type=qq_xnr_index_type, id=qq_number,  \
            body={"doc":{'qq_groups':qq_groups,}})
        result = 'Successfully changed'
    except:
        result = 'Changing Failed'
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



