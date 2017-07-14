#-*- coding:utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

from xnr.parameter import MAX_VALUE
from utils import show_group_info,search_by_keyword, search_by_xnr_number,\
                  search_by_speaker_number,search_by_speaker_nickname,\
                  search_by_period
from xnr.global_config import QQ_S_DATE

mod = Blueprint('qq_xnr_operate', __name__, url_prefix='/qq_xnr_operate')


# @mod.route('/show_group_info/')
# def ajax_show_group_info():
#     show_group_info()
#     return json.dumps(results)


@mod.route('/search_by_period/')
def ajax_search_by_period():
    # xnr_qq_number = request.args.get('xnr_number','')     #查询时需要给定虚拟人身份么
    startdate = request.args.get('startdate','')
    enddate = request.args.get('enddate','')
    results = search_by_period(startdate,enddate)
    return json.dumps(results)


@mod.route('/search_by_keyword/')
# 这个还没有写
def ajax_search_by_keyword():
    keyword = request.args.get('keyword','')
    date = QQ_S_DATE
    results = search_by_keyword(keyword,date)
    return json.dumps(results)


@mod.route('/search_by_xnr_number/')
def ajax_search_by_xnr_number():
    xnr_qq_number = request.args.get('xnr_number','')
    date = QQ_S_DATE
    results = search_by_xnr_number(xnr_qq_number, date)
    return json.dumps(results)


@mod.route('/search_by_xnr_nickname/')
def ajax_search_by_xnr_nickname():

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