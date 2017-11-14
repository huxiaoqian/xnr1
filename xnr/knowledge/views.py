#-*- coding:utf-8 -*-
import os
import time
import json
import pinyin
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect



mod = Blueprint('knowledge', __name__, url_prefix='/knowledge')

@mod.route('/domainLibrary/')
def domainLibrary():
    flag = request.args.get('flag','')
    return render_template('knowledge/domain_library.html',flag=flag)

@mod.route('/characterLibrary/')
def characterLibrary():
    flag = request.args.get('flag','')
    return render_template('knowledge/character_library.html',flag=flag)

@mod.route('/businessLibrary/')
def businessLibrary():
    flag = request.args.get('flag','')
    return render_template('knowledge/business_library.html',flag=flag)

@mod.route('/speechLibrary/')
def speechLibrary():
    flag = request.args.get('flag','')
    return render_template('knowledge/speech_library.html',flag=flag)
