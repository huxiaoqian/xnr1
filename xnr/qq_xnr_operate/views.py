#-*- coding:utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

from xnr.parameter import MAX_VALUE
from utils import show_group_info,search_by_keyword
from xnr.global_config import QQ_S_DATE

mod = Blueprint('qq_xnr_operate', __name__, url_prefix='/qq_xnr_operate')


@mod.route('/show_group_info/')
def ajax_show_group_info():
    show_group_info()
    return json.dumps(results)


@mod.route('/search_by_period/')
def ajax_search_by_period():

    return json.dumps(results)


@mod.route('/search_by_keyword/')
def ajax_search_by_keyword():
    keyword = request.args.get('keyword','')
    results = search_by_keyword(keyword)
    return json.dumps(results)


@mod.route('/search_by_xnr_number/')
def ajax_search_by_xnr_number():
    xnr_qq_number = request.args.get()
    date = QQ_S_DATE
    search_by_xnr_number(xnr_qq_number, date)
    return json.dumps(results)


@mod.route('/search_by_xnr_nickname/')
def ajax_search_by_xnr_nickname():

    return json.dumps(results)


@mod.route('/search_by_speaker_number/')
def ajax_search_by_speaker_number():

    return json.dumps(results)


@mod.route('/search_by_speaker_nickname/')
def ajax_search_by_speaker_nickname():

    return json.dumps(results)