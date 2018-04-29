#-*- coding:utf-8 -*-
import os
import time
import json
import sys
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

from xnr.parameter import MAX_VALUE
from utils import show_group_info,search_by_keyword, search_by_xnr_number,\
                  search_by_speaker_number,search_by_speaker_nickname,\
                  search_by_period,send_message,get_my_group, get_my_group_v2
from xnr.global_config import QQ_S_DATE
from xnr.time_utils import ts2datetime,datetime2ts,ts2date,date2ts
from xnr.qq.getgroup import getgroup_v2


mod = Blueprint('qq_xnr_operate', __name__, url_prefix='/qq_xnr_operate')


# @mod.route('/show_group_info/')
# def ajax_show_group_info():
#     show_group_info()
#     return json.dumps(results)

# http://219.224.134.213:9090/qq_xnr_operate/search_by_period/?xnr_number=1039598173&group_qq_name=%E6%88%BF%E5%B1%8B%E4%B9%B0%E5%8D%96%E8%BF%9D%E7%BA%A6%E7%BB%B4%E6%9D%83%E5%BE%8B%E5%B8%88%EF%BC%8C%E5%98%BF%E5%93%BC%E5%93%88&startdate=2018-03-01&enddate=2018-03-07
@mod.route('/search_by_period/')
def ajax_search_by_period():
    xnr_qq_number = request.args.get('xnr_number','')     #查询时需要给定虚拟人身份
    # group_qq_number = request.args.get('group_qq_number','')
    group_qq_name = request.args.get('group_qq_name','')  # 如果该群名有多个曾用群名（即：group_name的list中元素不止一个），以中文逗号'，'分隔。
                                                            # 或者是想要同时查询多个群的群名也是该url，需要把每个群的所有曾用群名都传进来
    startdate = request.args.get('startdate','')
    enddate = request.args.get('enddate','')
    results = search_by_period(xnr_qq_number,startdate,enddate,group_qq_name)
    return json.dumps(results)

#http://219.224.134.213:9090/qq_xnr_operate/search_by_xnr_number/?xnr_number=1039598173&group_qq_name=%E6%88%BF%E5%B1%8B%E4%B9%B0%E5%8D%96%E8%BF%9D%E7%BA%A6%E7%BB%B4%E6%9D%83%E5%BE%8B%E5%B8%88%EF%BC%8C%E5%98%BF%E5%93%BC%E5%93%88&date=2018-03-07
@mod.route('/search_by_xnr_number/')
def ajax_search_by_xnr_number():
    xnr_qq_number = request.args.get('xnr_number','')
    #group_qq_number = request.args.get('group_qq_number','')
    group_qq_name = request.args.get('group_qq_name','')   # 如果该群名有多个曾用群名（即：group_name的list中元素不止一个），以中文逗号'，'分隔。
                                                            # 或者是想要同时查询多个群的群名也是该url，需要把每个群的所有曾用群名都传进来
    date = request.args.get('date','')
    # ts = float(ts)
    # date = ts2datetime(ts)
    results = search_by_xnr_number(xnr_qq_number, date,group_qq_name)
    return json.dumps(results)

#http://219.224.134.213:9090/qq_xnr_operate/send_qq_group_message/?xnr_number=1039598173&group=房屋群&text=hhh
@mod.route('/send_qq_group_message/')
def send_qq_group_message():
    xnr_qq_number = request.args.get('xnr_number','')
    #group_qq_number = request.args.get('group_qq_number','')
    group = request.args.get('group','')  # 这里是群备注名！！！
    text = request.args.get('text','')
    results = send_message(xnr_qq_number,group, text)     #传入群汉字名称
    # results = False
    return json.dumps(results)

# http://219.224.134.213:9090/qq_xnr_operate/show_all_groups/?xnr_user_no=QXNR0007
@mod.route('/show_all_groups/')
def show_all_groups():
    xnr_user_no = request.args.get('xnr_user_no','')
    #groups = getgroup_v2(xnr_user_no)  没有必要再实时请求一遍目前所在的群，因为，在展示所有群的时候，必须保证已经在线了，已经更新过qq_xnr里的群了
    #my_group = get_my_group(xnr_user_no,groups)
    my_group = get_my_group_v2(xnr_user_no)

    return json.dumps(my_group)

# 暂时用不到的函数
@mod.route('/search_by_xnr_nickname/')
def ajax_search_by_xnr_nickname():
    results = False
    return json.dumps(results)


@mod.route('/search_by_speaker_number/')
def ajax_search_by_speaker_number():
    xnr_number = request.args.get('xnr_number','')
    speaker_number = request.args.get('speaker_number','')
    date = QQ_S_DATE
    results = search_by_speaker_number(xnr_number,speaker_number,date)
    return json.dumps(results)


@mod.route('/search_by_speaker_nickname/')
def ajax_search_by_speaker_nickname():
    xnr_number = request.args.get('xnr_number','')
    speaker_nickname = request.args.get('speaker_nickname','')
    date = QQ_S_DATE
    results = search_by_speaker_nickname(xnr_number,speaker_nickname,date)
    return json.dumps(results)

@mod.route('/search_by_keyword/')
def ajax_search_by_keyword():
    keyword = request.args.get('keyword','')
    # 暂时指定了日期 测试用
    date = '2017-07-13'
    results = search_by_keyword(keyword,date)
    return json.dumps(results)
