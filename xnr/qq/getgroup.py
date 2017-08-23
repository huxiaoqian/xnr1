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

if __name__ == '__main__':
    groups = getgroup()
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