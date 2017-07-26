#-*- coding:utf-8 -*-
import os
import time
import json
import pinyin
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect



mod = Blueprint('registered', __name__, url_prefix='/registered')

@mod.route('/socialAccounts/')
def socialAccounts():
    return render_template('registered/social_accounts.html')

@mod.route('/virtualCreated/')
def virtualCreated():
    return render_template('registered/virtual_created.html')
