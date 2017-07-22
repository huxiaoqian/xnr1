#-*- coding:utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

from xnr.global_utils import es_flow_text
from xnr.parameter import MAX_VALUE

from utils import search_by_xnr_number

mod = Blueprint('qq_xnr_monitor', __name__, url_prefix='/qq_xnr_monitor')


@mod.route('/show_sensitive_message/')
def ajax_show_sensitive_message():          #这两个函数二选一 用在最初始没指定时候显示
    results = show_sensitive_message()

    return json.dumps(results)


@mod.route('/search_by_xnr_number/')
def ajax_search_by_xnr_number():
    xnr_qq_number = request.args.get('xnr_number','')
    date = QQ_S_DATE
    results = search_by_xnr_number(xnr_qq_number, date)
    return json.dumps(results)




@mod.route('/search_by_period/')
def ajax_search_by_period():
    # xnr_qq_number = request.args.get('xnr_number','')     #查询时需要给定虚拟人身份么
    startdate = request.args.get('startdate','')
    enddate = request.args.get('enddate','')
    results = False
    return json.dumps(results)


@mod.route('/search_by_keyword/')
def ajax_search_by_keyword():
    keyword = request.args.get('keyword','')
    # 暂时指定了日期 测试用
    date = '2017-07-13'
    results = search_by_keyword(keyword,date)
    return json.dumps(results)

