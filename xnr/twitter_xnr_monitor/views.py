#-*- coding:utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

from xnr.parameter import MAX_VALUE
from xnr.time_utils import ts2datetime,datetime2ts,ts2date,date2ts

# from utils import 
 

mod = Blueprint('twitter_xnr_monitor', __name__, url_prefix='/twitter_xnr_monitor')