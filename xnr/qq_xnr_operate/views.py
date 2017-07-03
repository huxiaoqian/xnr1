#-*- coding:utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

from xnr.global_utils import es_flow_text


mod = Blueprint('qq_xnr_operate', __name__, url_prefix='/qq_xnr_operate')


@mod.route('/show_group_info/')
def ajax_show_group_info():
    
    return json.dumps(result)
