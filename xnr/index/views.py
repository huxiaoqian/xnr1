#-*- coding:utf-8 -*-
import os
import time
import json
import pinyin
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect



mod = Blueprint('index', __name__, url_prefix='/index')

@mod.route('/login/')
def login():
    return render_template('index/login.html')

@mod.route('/navigation/')
def navigation():
    return render_template('index/navigationMain.html')
