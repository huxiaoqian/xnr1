#-*- coding:utf-8 -*-

import json
import time
import datetime
from xnr.extensions import user_datastore
from xnr.time_utils import ts2datetime, ts2date
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect, make_response, g
from flask.ext.security import login_required, roles_required

mod = Blueprint('portrait', __name__, url_prefix='/index')

@mod.route('/navigationMain/')
def navigationMain():
    return render_template('navigationMain.html')

