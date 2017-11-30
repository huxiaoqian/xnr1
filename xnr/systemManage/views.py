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
    flag = request.args.get('flag','')
    return render_template('systemManage/daily.html',flag=flag)

@mod.route('/purview/')
def purview():
    flag = request.args.get('flag','')
    return render_template('systemManage/purview.html',flag=flag)

@mod.route('/virtual/')
def virtual():
    flag = request.args.get('flag','')
    return render_template('systemManage/virtual.html',flag=flag)

@mod.route('/userMange/')
def userMange():
    flag = request.args.get('flag','')
    return render_template('systemManage/userMange.html',flag=flag)
