#-*- coding:utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

from xnr.global_utils import es_flow_text

from utils import delete_weibo_xnr


mod = Blueprint('weibo_xnr_manage', __name__, url_prefix='/weibo_xnr_manage')


@mod.route('/add_weibo_xnr/')
def ajax_add_weibo_xnr():
    results = True
    return json.dumps(result)


@mod.route('/delete_weibo_xnr/')
def ajax_delete_weibo_xnr():
	user_no=request.args.get('user_no','')
    results = delete_weibo_xnr(user_no)
    return json.dumps(results)

@mod.route('/show_weibo_xnr/')
def ajax_show_weibo_xnr():
    results = True
    return json.dumps(results)

