# -*- coding: utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect
from xnr.parameter import MAX_VALUE
from xnr.time_utils import ts2datetime,datetime2ts,ts2date,date2ts
from utils import utils_text_trans, utils_voice_trans

mod = Blueprint('wx_xnr_trans', __name__, url_prefix='/wx_xnr_trans')

@mod.route('/text_trans/')
def text_trans():
    q_str = request.args.get('q', '')
    if q_str:
        q = q_str.split(',')
        res = utils_text_trans(q)
        if res:
            return json.dumps(res)
    return None 


@mod.route('/voice_trans/')
def voice_trans():
    voice_path = request.args.get('voice_path', '')
    if voice_path:
        #get voice
        voice = None
        #voice trans
        res = utils_voice_trans(voice)
        if res:
            return json.dumps(res)
    return None 