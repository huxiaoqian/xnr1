# -*- coding: utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect
from xnr.parameter import MAX_VALUE
from xnr.global_config import WX_S_DATE
from xnr.time_utils import ts2datetime,datetime2ts,ts2date,date2ts
from utils import utils_load_groups, utils_search_by_group_puid, utils_send_msg

mod = Blueprint('wx_xnr_operate', __name__, url_prefix='/wx_xnr_operate')

@mod.route('/sendmsg/')
def send_msg():
    wxbot_id = request.args.get('wxbot_id', '')
    msg = request.args.get('msg', '')
    group_list_string = request.args.get('group_list', '')
    group_list = group_list_string.split(',')
    if wxbot_id and msg and group_list:
        res = utils_send_msg(wxbot_id=wxbot_id, puids=group_list, msg=msg)
        if res:
            return json.dumps(res)
    return None

@mod.route('/loadgroups/')
def load_groups():
    wxbot_id = request.args.get('wxbot_id', '')
    if wxbot_id:
        res = utils_load_groups(wxbot_id)
        if res:
            return json.dumps(res)
    return None 

#默认加载最近*天的数据
@mod.route('/searchbygrouppuid/')   
def search_by_group_puid():
    wxbot_id = request.args.get('wxbot_id', '')
    group_puid = request.args.get('group_puid', '')
    period = request.args.get('period', '')
    startdate = request.args.get('startdate', '')   #str 2017-10-15
    enddate = request.args.get('enddate', '')
    if wxbot_id and group_puid:
        if period or (startdate and enddate):
            res = utils_search_by_group_puid(wxbot_id, group_puid, period, startdate, enddate)
            if res:
                return json.dumps(res)
    return None