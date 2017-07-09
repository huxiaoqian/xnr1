#-*- coding:utf-8 -*-
import os
import time
import datetime
import json
from flask import Blueprint,url_for,render_template,request,\
        abort,flash,session,redirect

from xnr.global_utils import es_flow_text
from utils import show_weiboxnr_content,lookup_weiboxnr_keywordslist,lookup_weibo_info,\
        count_weiboxnr_keyword

mod=Blueprint('weibo_xnr_monitor',__name__,url_prefix='/weibo_xnr_monitor')

#lookup weibo_xnr test,can be delete
@mod.route('/lookup_weiboxnr_test/')
def ajax_lookup_weiboxnr_test():
   # uid=request.args.get('uid','')
    results={}
    results=show_weiboxnr_content()
    return json.dumps(results)

#lookup weibo keywordslist test
@mod.route('/lookup_weibo_keywords/')
def ajax_lookup_weibo_keywords():
    results={}
    results=lookup_weiboxnr_keywordslist()
    return json.dumps(results)

#lookup weibo info
@mod.route('/lookup_weibo_info/')
def ajax_lookup_weibo_info():
    results={}
    ts_first='2016/11/15 10:27:12'
    ts_second='2016/11/15 10:27:14'
    firsttime=datetime.datetime.strptime(ts_first,'%Y/%m/%d %H:%M:%S')
    secondtime=datetime.datetime.strptime(ts_second,'%Y/%m/%d %H:%M:%S')
    userlist=[3033874187,2604977652,3936969641,3964892488]
    results=lookup_weibo_info(firsttime,secondtime,userlist)
    word_list=count_weiboxnr_keyword(results)
   # print results
   # for r in results:
   #     print r
   # print word_list
   # for w in word_list:
   #     print w
    return json.dumps(word_list)

