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
    return render_template('knowledge/domain_library.html')

@mod.route('/characterLibrary/')
def characterLibrary():
    return render_template('knowledge/character_library.html')

@mod.route('/businessLibrary/')
def businessLibrary():
    return render_template('knowledge/business_library.html')

@mod.route('/speechLibrary/')
def speechLibrary():
    return render_template('knowledge/speech_library.html')
