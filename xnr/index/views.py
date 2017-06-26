#-*- coding:utf-8 -*-

import json
import time
import datetime
from xnr.extensions import user_datastore
from xnr.time_utils import ts2datetime, ts2date
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect, make_response, g
from flask.ext.security import login_required, roles_required

mod = Blueprint('portrait', __name__, url_prefix='/index')

"""
@mod.route('/')
@login_required
@roles_required("overview")
def loading():
    return render_template('portrait/overview.html')
"""
@mod.route('/user_rank/')
@login_required
@roles_required("userrank")
def user_rank():
    return render_template('portrait/user_rank.html')

@mod.route('/mood_detect/')
@login_required
@roles_required("sentiment")
def mood_detect():
    return render_template('portrait/mood_detect.html')

@mod.route('/social_sensing/')
@login_required
@roles_required("socialsensing")
def social_sensing():
    return render_template('portrait/social_sensing.html')

@mod.route('/sensing_analysis/')
@login_required
@roles_required("socialsensing")
def sensing_analysis():
    task_name = request.args.get('task_name','监督维权律师' )
    keywords = request.args.get('keywords','律师,维权' )
    ts = request.args.get('ts','1378567800' )
    return render_template('portrait/sensing_analysis.html', task_name=task_name, keywords=keywords, ts=ts)

@mod.route('/group/')
@login_required
@roles_required("group")
def group_identify():
    return render_template('portrait/group_identify.html')

@mod.route('/group_list/')
@login_required
@roles_required("group")
def group_list():
    return render_template('portrait/group_list.html')

@mod.route('/group_analysis/')
@login_required
@roles_required("group")
def group_analysis():
    name = request.args.get('name', 'test_task')

    return render_template('portrait/group_analysis.html', name=name)
@mod.route('/contrast/')
@login_required
@roles_required("profile")
def contrast():
    
    return render_template('portrait/compare.html')

@mod.route('/personal/')
@login_required
@roles_required("profile")
def personal():
    uid = request.args.get('uid', '1642591402')

    return render_template('portrait/personal.html', uid=uid)

@mod.route('/personal_detail/')
@login_required
@roles_required("profile")
def personal_detail():
    uid = request.args.get('uid', '1642591402')

    return render_template('portrait/personal_detail.html', uid=uid)

@mod.route('/recommend_in_out/')
@login_required
@roles_required("administration")
def recommend_in_out():

    return render_template('portrait/recommend_in_out.html')
"""
@mod.route('/recommend_in/')
def recommend_in():

    return render_template('portrait/recommend_in.html')

@mod.route('/recommend_out/')
def recommend_out():

    return render_template('portrait/recommend_out.html')
"""
@mod.route('/influence_rank/')
def influence_rank():

    return render_template('portrait/influence_rank.html')
@mod.route('/tag/')
@login_required
def tag():

    return render_template('portrait/tag.html')
@mod.route('/contrast_analysis/')
@login_required
@roles_required("profile")
def contrast_analysis():
    return render_template('portrait/contrast_analysis.html')

@mod.route('/portrait_in/')
@login_required
@roles_required("profile")
def portrait_in():
    return render_template('portrait/portrait_in.html')

@mod.route('/search_portrait/')
@login_required
@roles_required("profile")
def search_portrait():
    return render_template('portrait/search_portrait.html')

@mod.route('/search_contrast/')
@login_required
@roles_required("profile")
def search_contrast():
    return render_template('portrait/search_contrast.html')

@mod.route('/search_connect/')
@login_required
@roles_required("profile")
def search_connect():
    return render_template('portrait/search_connect.html')
'''
@mod.route('/search_result/')
def search_result():
    stype = request.args.get('stype', '1')
    if stype == '1':
        term = request.args.get('term', '')
        #print term
        return render_template('portrait/search_result.html', stype=stype, term=term)
    else:
        uid = request.args.get('uid', '')
        uname = request.args.get('uname', '')
        location = request.args.get('location', '')
        activity_geo = request.args.get('activity_geo', '')
        adkeyword = request.args.get('adkeyword', '')
        hashtag = request.args.get('hashtag', '')
        psycho_status_by_emotion = request.args.get('psycho_status_by_emotion', '')
        psycho_status_by_word = request.args.get('psycho_status_by_word','')
        psycho_feature = request.args.get('psycho_feature', '')
        domain = request.args.get('domain', '')
        topic = request.args.get('topic', '')
        tag = request.args.get('tag', '')

        return render_template('portrait/search_result.html', stype=stype, uid=uid, uname=uname,\
                location=location, activity_geo=activity_geo, adkeyword=adkeyword, hashtag=hashtag, psycho_status_by_emotion=psycho_status_by_emotion,psycho_status_by_word=psycho_status_by_word,\
                psycho_feature=psycho_feature, domain=domain, topic=topic, tag=tag)

'''
@mod.route('/contact/')
@login_required
@roles_required("profile")
def contact():
    uid = request.args.get('uid', '2001627641')
    return render_template('portrait/contact.html', uid=uid)

@mod.route('/usercenter/')
@login_required
def usercenter():
    return render_template('portrait/usercenter.html')

@mod.route('/role_manage/')
@login_required
@roles_required("administration")
def role_manage():
    return redirect("/admin")
    #return render_template('portrait/role_manage.html')

@mod.route('/logmanage/')
@login_required
@roles_required("administration")
def logmanage():
    return redirect("http://114.255.183.77:5601/")


@mod.route('/network/')
def net():
    return render_template('portrait/net.html')
