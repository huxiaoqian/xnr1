# -*-coding:utf-8-*-
import os
import pinyin
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect
from utils import domain_create_task,get_domain_info,get_role_info


mod = Blueprint('knowledge_management',__name__,url_prefix='/knowledge_management')

@mod.route('/create_domain/')
def ajax_create_domain():
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

