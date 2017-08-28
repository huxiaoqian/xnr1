# -*- coding: utf-8 -*-
'''
use to save function---about deal database
'''
import sys
from xnr.global_utils import es_xnr,qq_xnr_index_name,qq_xnr_index_type
from xnr.parameter import MAX_VALUE,LOCALHOST_IP
import socket
from xnr.qq.getgroup import getgroup_v2

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
    qq_number = xnr_info['qq_number']
    qq_groups = xnr_info['qq_groups']
    nickname = xnr_info['nickname']
    # active_time = xnr_info[3]
    create_ts = xnr_info['create_ts']
    exist_port_list = get_all_ports()           #返回list形式int型端口号
    qqbot_port = find_port(exist_port_list)
    qq_groups_num = len(qq_groups.split(','))
    # qq_groups = getgroup_v2(qq_number)
    try:
        # if es_xnr.get(index=qq_xnr_index_name, doc_type=qq_xnr_index_type, id=qq_number):
        #     return 0
        es_xnr.index(index=qq_xnr_index_name, doc_type=qq_xnr_index_type, id=qq_number, \
        body={'qq_number':qq_number,'nickname':nickname,'qq_groups':qq_groups,'create_ts':create_ts,\
                'qqbot_port':qqbot_port,'qq_groups_num':qq_groups_num})
        result = 1
    except:
        result = 0
    return result

def show_qq_xnr(MAX_VALUE):
    query_body = {
        'query':{
            'match_all':{}
        },
    }
    results = []
    result = es_xnr.search(index=qq_xnr_index_name, doc_type=qq_xnr_index_type, body=query_body)['hits']['hits']
    for item in result:
        temp = item['_source'].copy()
        results.append(temp)
    
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



