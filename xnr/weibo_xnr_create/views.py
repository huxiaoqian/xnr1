#-*- coding:utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect


mod = Blueprint('weibo_xnr_create', __name__, url_prefix='/weibo_xnr_create')


@mod.route('/create_weibo_xnr/')
def ajax_create_weibo_xnr():
    
    return json.dumps(result)

@mod.route('/show_register_info/')
def ajax_show_register_info():
    
    return json.dumps(results)

@mod.route('/save_register_info/')
def ajax_save_register_info():

    return json.dumps(results)

@mod.route('/bind_info/')
def ajax_bind_indo():

    return json.dumps(results)
