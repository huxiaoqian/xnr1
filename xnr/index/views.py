#-*- coding:utf-8 -*-
import os
import time
import json
import pinyin
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

from xnr.extensions import db, user_datastore


mod = Blueprint('index', __name__, url_prefix='/index')

@mod.route('/login/')
def login():
    return render_template('index/login.html')

@mod.route('/navigation/')
def navigation():
    return render_template('index/navigationMain.html')

@mod.route('/navigationQQ/')
def navigationQQ():
    return render_template('index/navigationMain_QQ.html')

@mod.route('/navigationFaceBook/')
def navigationFaceBook():
    return render_template('index/navigationFaceBook.html')

@mod.route('/navigationTwitter/')
def navigationTwitter():
    return render_template('index/navigationTwitter.html')

@mod.route('/navigationWX/')
def navigationWX():
    return render_template('index/navigationMain_WX.html')


@mod.route('/create_account/')
def ajax_create_account():

    account_name = request.args.get('account_name','')
    password = request.args.get('password','')

    try:
        db.create_all()
        #role_1 = user_datastore.create_role(name='userrank', description=u'用户排行模块权限')
        user_1 = user_datastore.create_user(email=account_name, password=password)

        #user_datastore.add_role_to_user(user_1, role_1)
        #user_datastore.add_role_to_user(user_1, role_2)
        db.session.commit()
        return "success"
    except:
        db.session.rollback()
        return "failure"
