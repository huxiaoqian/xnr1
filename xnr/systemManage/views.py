#-*- coding:utf-8 -*-
import os
import time
import json
import pinyin
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect



mod = Blueprint('systemManage', __name__, url_prefix='/systemManage')

@mod.route('/daily/')
def daily():
    return render_template('systemManage/daily.html')

@mod.route('/purview/')
def purview():
    return render_template('systemManage/purview.html')

@mod.route('/virtual/')
def virtual():
    return render_template('systemManage/virtual.html')