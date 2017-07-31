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

@mod.route('/posting/')
def posting():
    return render_template('control/posting.html')

@mod.route('/postingQQ/')
def postingQQ():
    return render_template('control/postingQQ.html')

@mod.route('/socialFeedback/')
def socialFeedback():
    return render_template('control/social_feedback.html')

@mod.route('/activeSocialization/')
def activeSocialization():
    return render_template('control/active_socialization.html')

