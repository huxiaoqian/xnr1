# -*-coding:utf-8-*-
import os
import time
import json
import pinyin
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

mod = Blueprint('weibo_xnr_knowledge_base_management', __name__, url_prefix='/weibo_xnr_knowledge_base_management')

#根据
@mod.route('/create_weibo_xnr/')
def ajax_create_weibo_xnr():
    
    domain_name =  request.args.get('domain_name','')
    domain_pinyin = pinyin.get(domain_name,format='strip',delimiter='_')
    domain_info = get_domain_info(domain_pinyin)
    
    return json.dumps(domain_info)

@mod.route('/show_role_info/')
def ajax_show_role_info():
    domain_name = request.args.get('domain_name','')
    domain_pinyin = pinyin.get(domain_name,format='strip',delimiter='_')
    role_name = request.args.get('role_name','')
    role_info = get_role_info(domain_pinyin,role_name)

    return json.dumps(role_info)
