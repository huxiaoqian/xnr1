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
                  search_by_period,send_message
from xnr.global_config import QQ_S_DATE
from xnr.time_utils import ts2datetime,datetime2ts,ts2date,date2ts
from xnr.qq.getgroup import getgroup

mod = Blueprint('qq_xnr_operate', __name__, url_prefix='/qq_xnr_operate')


# @mod.route('/show_group_info/')
# def ajax_show_group_info():
#     show_group_info()
#     return json.dumps(results)


@mod.route('/search_by_period/')
def ajax_search_by_period():
    xnr_qq_number = request.args.get('xnr_number','')     #查询时需要给定虚拟人身份么
    startdate = request.args.get('startdate','')
    enddate = request.args.get('enddate','')
    results = search_by_period(xnr_qq_number,startdate,enddate)
    return json.dumps(results)





@mod.route('/search_by_xnr_number/')
def ajax_search_by_xnr_number():
    xnr_qq_number = request.args.get('xnr_number','')
    ts = request.args.get('date','')
    ts = float(ts)
    date = ts2datetime(ts)
    results = search_by_xnr_number(xnr_qq_number, date)
    return json.dumps(results)

@mod.route('/send_qq_group_message/')
def send_qq_group_message():
    # xnr_qq_number = request.args.get('xnr_number','')
    group = request.args.get('group','')
    text = request.args.get('text','')
    results = send_message(group, text)     #传入群汉字名称
    # results = False
    return json.dumps(results)

@mod.route('/show_all_groups/')
def show_all_groups():
    groups = getgroup()
    return json.dumps(groups)




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