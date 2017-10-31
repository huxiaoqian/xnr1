#-*- coding:utf-8 -*-
import os
import time
import json
import pinyin
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect



mod = Blueprint('personalCenter', __name__, url_prefix='/personalCenter')

@mod.route('/individual/')
def personal_center():
    return render_template('personalCenter/personal_center.html')

@mod.route('/individualQQ/')
def personal_centeQQ():
    return render_template('personalCenter/personal_centerQQ.html')

@mod.route('/individualTwitter/')
def individualTwitter():
    return render_template('personalCenter/personal_centerTwitter.html')

@mod.route('/individualWX/')
def personal_centeWX():
    return render_template('personalCenter/personal_centerWX.html')

