# -*- coding: utf-8 -*-
# 用于获取登录用户的群列表
import json
import subprocess
from qqbot import _bot as bot
from qqbot.utf8logger import INFO
import sys
sys.path.append('../')
from global_utils import es_xnr as es,qq_xnr_index_name,qq_xnr_index_type

def getgroup():
    result = {}
    try:
        groups = bot.List('group')
    except:
        bot.Login()
        groups = bot.List('group')
    if groups != [] and groups != 'None':
        for group in groups:
            group_name = group.name
            group_number = group.qq
            result[group_number]=group_name
    return result

def getgroup_v2(qq_xnr):
    group_dict = {}
    #step0: get qqbot_port
    if qq_xnr[:4] != 'QXNR':

        search_result = es.search(index=qq_xnr_index_name,doc_type=qq_xnr_index_type,\
            body={'query':{'term':{'qq_number':qq_xnr}}})['hits']['hits']

        qq_xnr = search_result[0]['_id']

    #try:
    qq_xnr_es_result = es.get(index=qq_xnr_index_name,\
            doc_type=qq_xnr_index_type, id=qq_xnr, _source=True)['_source']

    group_info = json.loads(qq_xnr_es_result['group_info'])
    
    qqbot_port = qq_xnr_es_result['qqbot_port']
    print 'qqbot_port..',qqbot_port
    p_str = 'qq ' + str(qqbot_port) + ' list group'
    p = subprocess.Popen(p_str, shell=True, \
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    line_count = 0
    for line in p.stdout.readlines():
        line_count += 1
        print 'line.==========',line    
        if line_count >= 5 and line_count%2==1:
            item_line_list = line.split('|')
            
            try:
                #qq_group_number = str(int(item_line_list[2]))
                qq_uin_number = str(int(item_line_list[7]))
                print 'qq_uin_number..',qq_uin_number
                qq_group_name = item_line_list[4]
                qq_mark_name = item_line_list[5]
                # group_dict[qq_group_number] = qq_group_name
                group_dict[qq_uin_number] = qq_group_name

                # 如果uin为空，则添加进去uin，如果不为空，则更新群名（因为群名可能修改）
                for key,value_dict in group_info.iteritems():
                    
                    mark_name = value_dict['mark_name']

                    if not qq_mark_name:
                        if qq_mark_name == mark_name:
                            if not qq_group_name in value_dict['group_name']:
                                group_info[key]['group_name'].append(qq_group_name)

            except:
                next

    group_info = json.dumps(group_info)
    es.update(index=qq_xnr_index_name,doc_type=qq_xnr_index_type,id=qq_xnr,body={'doc':{'group_info':group_info}})
    
    print 'group_dict::',group_dict

    return group_dict

# 定时更新uin对应的群名
def update_group_name():

    query_body = {
        'query':{
            'match_all':{}
        },
        'size':MAX_VALUE
    }
    
    result = es.search(index=qq_xnr_index_name, doc_type=qq_xnr_index_type, body=query_body)['hits']['hits']
    qq_xnr_list = []
    for item in result:
        xnr_user_no = item['_source']['xnr_user_no']
        getgroup_v2(xnr_user_no)


if __name__ == '__main__':
    
    update_group_name() 
    #groups = getgroup()
    #qq_xnr = 'QXNR0001'
    #groups = getgroup_v2(qq_xnr)
    # for group in groups:
    #     group_name = group.name
    #     group_number = group.qq
    # print group
    # print type(group[0])
    # print dir(group[0])
    # print(group[0].name)
    # print(group[0].qq)
    #print groups
#     [2017-08-22 10:51:25] [INFO] 请在其他终端使用 qq 命令来控制 QQBot ，示例： qq send buddy jack hello
# [2017-08-22 10:51:30] [ERROR] 无法和腾讯服务器建立私密连接， 5 秒后将尝试使用非私密连接和腾讯服务器 通讯。若您不希望使用非私密连接，请按 Ctrl+C 退出本程序。
