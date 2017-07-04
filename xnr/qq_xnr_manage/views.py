#-*- coding:utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

from xnr.global_utils import es_flow_text
from utils import show_qq_xnr


mod = Blueprint('qq_xnr_manage', __name__, url_prefix='/qq_xnr_manage')


@mod.route('/add_qq_xnr/')
def ajax_add_qq_xnr():
    results = True
    return json.dumps(results)


@mod.route('/delete_qq_xnr/')
def ajax_delete_qq_xnr():
    results = True
    return json.dumps(results)

@mod.route('/show_qq_xnr/')
def ajax_show_qq_xnr():
    results = {}
    task_name = request.args.get('task_name','')
    results = show_qq_xnr(task_name)
    return json.dumps(results)

