#-*- coding:utf-8 -*-
import os
import time
import datetime
import json
from flask import Blueprint,url_for,render_template,request,\
        abort,flash,session,redirect

mod=Blueprint('wx_xnr_warning',__name__,url_prefix='/wx_xnr_warning')