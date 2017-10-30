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
