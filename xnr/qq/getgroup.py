# -*- coding: utf-8 -*-
# 用于获取登录用户的群列表

from qqbot import _bot as bot
from qqbot.utf8logger import INFO

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
    try:
        qq_xnr_es_result = es.get(index_name=qq_xnr_index_name,\
                doc_type=qq_xnr_index_type, id=qq_xnr, _source=True)['_source']
    except:
        print 'qq_xnr is not exist'
        return group_dict
    #step1: get group list
    qqbot_port = qq_xnr_es_result['qqbot_port']
    p_str = 'qq ' + qqbot_port + ' list group'
    p = subprocess.Popen(p_str, shell=True, \
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    line_count = 0
    for line in p.stdout.readlines():
        line_count += 1
        if line_count >= 5 and line_count%2==1:
            item_line_list = line.split('|')
            qq_group_number = str(int(item_line_list[2]))
            qq_group_name = item_line_list[3]
            group_dict[qq_group_number] = qq_group_name
    return group_dict

if __name__ == '__main__':
    groups = getgroup(qq_xnr)
    groups = getgroup_v2()
    # for group in groups:
    #     group_name = group.name
    #     group_number = group.qq
    # print group
    # print type(group[0])
    # print dir(group[0])
    # print(group[0].name)
    # print(group[0].qq)
    print groups
#     [2017-08-22 10:51:25] [INFO] 请在其他终端使用 qq 命令来控制 QQBot ，示例： qq send buddy jack hello
# [2017-08-22 10:51:30] [ERROR] 无法和腾讯服务器建立私密连接， 5 秒后将尝试使用非私密连接和腾讯服务器 通讯。若您不希望使用非私密连接，请按 Ctrl+C 退出本程序。
