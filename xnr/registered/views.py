#-*- coding:utf-8 -*-
import os
import time
import json
import pinyin
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect
mod = Blueprint('registered', __name__, url_prefix='/registered')

@mod.route('/targetCustom/')
def targetCustom():
    flag = request.args.get('flag','')
    return render_template('registered/target_custom.html',flag=flag)

@mod.route('/virtualCreated/')
def virtualCreated():
    flag = request.args.get('flag','')
    return render_template('registered/virtual_created.html',flag=flag)
    
@mod.route('/socialAccounts/')
def socialAccounts():
    flag = request.args.get('flag','')
    return render_template('registered/social_accounts.html',flag=flag)

