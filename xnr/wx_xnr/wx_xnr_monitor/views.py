# -*- coding: utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect
from xnr.wx_xnr.parameter import MAX_VALUE
from xnr.wx_xnr.time_utils import ts2datetime,datetime2ts,ts2date,date2ts
from utils import utils_search

mod = Blueprint('wx_xnr_monitor', __name__, url_prefix='/wx_xnr_monitor')

#默认加载最近30天的数据
@mod.route('/search/')
def search():
    wxbot_id = request.args.get('wxbot_id', '')
    startdate = request.args.get('startdate', '')	#str 2017-10-15
    enddate = request.args.get('enddate', '')
    if wxbot_id:
        res = utils_search(wxbot_id, startdate, enddate)
        if res:
            return json.dumps(res)
    return None