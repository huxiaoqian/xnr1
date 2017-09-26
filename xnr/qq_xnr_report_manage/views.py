#-*- coding:utf-8 -*-
import os
import time
import datetime
import json
from flask import Blueprint,url_for,render_template,request,\
        abort,flash,session,redirect

#from xnr.global_utils import 
#from utils import 

mod=Blueprint('qq_xnr_report_manage',__name__,url_prefix='/qq_xnr_report_manage')
