#-*- coding:utf-8 -*-
import os
import time
import json
import pinyin
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect



mod = Blueprint('control', __name__, url_prefix='/control')

@mod.route('/operationControl/')
def operationControl():
    return render_template('control/operation_control.html')

@mod.route('/operationTwitter/')
def operationTwitter():
    return render_template('control/operationTwitter.html')

@mod.route('/operationFaceBook/')
def operationFaceBook():
    return render_template('control/operationFaceBook.html')

@mod.route('/posting/')
def posting():
    return render_template('control/posting.html')

@mod.route('/postingQQ/')
def postingQQ():
    QQ_id = request.args.get('QQ_id','')
    QQ_num = request.args.get('QQ_num','')
    return render_template('control/postingQQ.html',QQ_id=QQ_id,QQ_num=QQ_num)

@mod.route('/postingWX/')
def postingWX():
    WXbot_id = request.args.get('WXbot_id','')
    # QQ_num = request.args.get('QQ_num','')
    # return render_template('control/postingWX.html',QQ_id=QQ_id,QQ_num=QQ_num)
    return render_template('control/postingWX.html',WXbot_id=WXbot_id)

@mod.route('/postingTwitter/')
def postingTwitter():
    return render_template('control/postingTwitter.html')

@mod.route('/postingFaceBook/')
def postingFaceBook():
    return render_template('control/postFaceBook.html')

@mod.route('/socialFeedback/')
def socialFeedback():
    return render_template('control/social_feedback.html')

@mod.route('/socialFeedbackTwitter/')
def socialFeedbackTwitter():
    return render_template('control/social_feedbackTwitter.html')

@mod.route('/socialFeedbackFaceBook/')
def socialFeedbackFaceBook():
    return render_template('control/social_feedbackFaceBook.html')

@mod.route('/activeSocialization/')
def activeSocialization():
    return render_template('control/active_socialization.html')

@mod.route('/activeSocializationTwitter/')
def activeSocializationTwitter():
    return render_template('control/active_socializationTwitter.html')

@mod.route('/activeSocializationFaceBook/')
def activeSocializationFaceBook():
    return render_template('control/active_socializationFaceBook.html')
