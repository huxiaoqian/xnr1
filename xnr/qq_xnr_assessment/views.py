#-*- coding: utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

from xnr.global_utils import es_flow_text
from utils import get_influence_mark

mod = Blueprint('qq_xnr_assessment', __name__, url_prefix='/qq_xnr_assessment')

# 影响力评估
@mod.route('/influence_mark/')
def ajax_influence_mark():
	xnr_user_no = request.args.get('xnr_user_no','')
	results = get_influence_mark(xnr_user_no)

	return json.dumps(results)

@mod.route('/show_safe_feature/')
def ajax_show_safe_feature():
    results = True
    return json.dumps(results)
