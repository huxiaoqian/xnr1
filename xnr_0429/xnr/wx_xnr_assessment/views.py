# -*- coding: utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect
from xnr.parameter import MAX_VALUE
from xnr.global_config import WX_S_DATE
from xnr.time_utils import ts2datetime,datetime2ts,ts2date,date2ts
from utils import utils_get_influence, utils_get_penetration, utils_get_safe

mod = Blueprint('wx_xnr_assessment', __name__, url_prefix='/wx_xnr_assessment')

#影响力评估，默认加载最近7天的数据
@mod.route('/influence/')
def get_influence():
    wxbot_id = request.args.get('wxbot_id', '')
    period = request.args.get('period', '')
    startdate = request.args.get('startdate', '')   #str 2017-10-15
    enddate = request.args.get('enddate', '')
    if wxbot_id:
        if period or (startdate and enddate):
            res = utils_get_influence(wxbot_id, period, startdate, enddate)
            if res:
                return json.dumps(res)
    return json.dumps({}) 

#渗透力，默认加载最近7天的数据
@mod.route('/penetration/')
def get_penetration():
    wxbot_id = request.args.get('wxbot_id', '')
    period = request.args.get('period', '')
    startdate = request.args.get('startdate', '')   #str 2017-10-15
    enddate = request.args.get('enddate', '')
    if wxbot_id:
        if period or (startdate and enddate):
            res = utils_get_penetration(wxbot_id, period, startdate, enddate)
            if res:
                return json.dumps(res)
    return json.dumps({}) 

#安全性，默认加载最近7天的数据
@mod.route('/safe/')
def get_safe():
    wxbot_id = request.args.get('wxbot_id', '')
    period = request.args.get('period', '')
    startdate = request.args.get('startdate', '')   #str 2017-10-15
    enddate = request.args.get('enddate', '')
    if wxbot_id:
        if period or (startdate and enddate):
            res = utils_get_safe(wxbot_id, period, startdate, enddate)
            if res:
                return json.dumps(res)
    return json.dumps({}) 