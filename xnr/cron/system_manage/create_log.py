#-*- coding: utf-8 -*-
'''
log management function
'''
import os
import json
import time
import sys
reload(sys)
sys.path.append('../../')
import sqlite
import sqlite3

#连接数据库,获取账户列表
def get_user_account_list():     
    cx = sqlite3.connect("/home/ubuntu8/yuanhuiru/xnr/xnr1/xnr/flask-admin.db")
    cu=cx.cursor()
    cu.execute("select email from user") 
    user_info = cu.fetchall()
    cx.close()
    return user_info

#日志生成文件组织
def create_user_log():
    user_name_list=get_user_account_list()
    
#日志文件操作内容模块

