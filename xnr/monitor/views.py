#-*- coding:utf-8 -*-
import os
import time
import json
import pinyin
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect



mod = Blueprint('monitor', __name__, url_prefix='/monitor')

@mod.route('/characterBehavior/')
def characterBehavior():
    return render_template('monitor/character_behavior.html')

@mod.route('/speechContent/')
def speechContent():
    return render_template('monitor/speech_content.html')

@mod.route('/eventEmerges/')
def eventEmerges():
    return render_template('monitor/event_emerges.html')

@mod.route('/timeWarning/')
def timeWarning():
    return render_template('monitor/time_warning.html')
