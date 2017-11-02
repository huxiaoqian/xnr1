#-*- coding:utf-8 -*-
import os
import time
import json
import pinyin
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect



mod = Blueprint('behavioGauge', __name__, url_prefix='/behavioGauge')

@mod.route('/influeAssess/')
def influeAssess():
    return render_template('behavioGauge/influe_assess.html')

@mod.route('/penetration/')
def penetration():
    return render_template('behavioGauge/penetration.html')

@mod.route('/safe/')
def safe():
    return render_template('behavioGauge/safe.html')

@mod.route('/behaviorQQ/')
def behaviorQQ():
    return render_template('behavioGauge/behaviorQQ.html')

@mod.route('/behaviorWX/')
def behaviorWX():
    return render_template('behavioGauge/behaviorWX.html')

@mod.route('/influeAssessTwitter/')
def influeAssessTwitter():
    return render_template('behavioGauge/influe_assessTwitter.html')

@mod.route('/penetrationTwitter/')
def penetrationTwitter():
    return render_template('behavioGauge/penetrationTwitter.html')

@mod.route('/safeTwitter/')
def safeTwitter():
    return render_template('behavioGauge/safeTwitter.html')

@mod.route('/influeAssessFaceBook/')
def influeAssessFaceBook():
    return render_template('behavioGauge/influe_assessFaceBook.html')

@mod.route('/penetrationFaceBook/')
def penetrationFaceBook():
    return render_template('behavioGauge/penetrationFaceBook.html')

@mod.route('/safeFaceBook/')
def safeFaceBook():
    return render_template('behavioGauge/safeFaceBook.html')    
