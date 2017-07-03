#-*- coding: utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
        abort, flash, session, redirect
from xnr.global_utils import es_flow_text

mod = Blueprint('weibo_xnr_assessment', __name__, url_prefix='/weibo_xnr_assessment')


@mod.route('/show_safe_feature/')
def ajax_show_safe_feature():
    results = True
    return json.dumps(results)
