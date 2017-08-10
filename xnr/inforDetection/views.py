#-*- coding:utf-8 -*-
import os
import time
import json
import pinyin
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect



mod = Blueprint('inforDetection', __name__, url_prefix='/inforDetection')

@mod.route('/inforChecking/')
def inforChecking():
    return render_template('inforDetection/inforChecking.html')

@mod.route('/inforCheckingQQ/')
def inforCheckingQQ():
    return render_template('inforDetection/inforCheckingQQ.html')
