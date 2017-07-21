#-*- coding:utf-8 -*-
import os
import time
import json
import pinyin
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect



mod = Blueprint('control', __name__, url_prefix='/control')

@mod.route('/operationControl/')
def operationControl():
    return render_template('control/operation_control.html')

