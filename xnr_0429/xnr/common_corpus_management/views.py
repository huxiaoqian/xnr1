# # -*-coding:utf-8-*-
# import os
# import time
# import json
# import pinyin
# from flask import Blueprint, url_for, render_template, request,\
#                   abort, flash, session, redirect

# from utils import show_facebook_corpus

# mod = Blueprint('common_corpus_management', __name__, url_prefix='/common_corpus_management')


# @mod.route('/show_facebook_corpus/')
# def ajax_show_facebook_corpus():
#     task_detail = dict()
#     task_detail['create_type'] = request.args.get('create_type','') #my_xnrs,all_xnrs
#     task_detail['corpus_status'] = int(request.args.get('corpus_status',''))    #如果是初始进入为0，其他为1
#     task_detail['request_type'] = request.args.get('request_type','') #all,one
#     task_detail['theme_type_1'] = request.args.get('theme_type_1','').split(',')
#     task_detail['theme_type_2'] = request.args.get('theme_type_2','').split(',')
#     task_detail['theme_type_3'] = request.args.get('theme_type_3','').split(',')
#     results = show_facebook_corpus(task_detail)
#     return json.dumps(results)