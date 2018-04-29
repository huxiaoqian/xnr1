#-*- coding:utf-8 -*-
import os
import time
import json
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

#from utils import 

mod = Blueprint('facebook_xnr_community', __name__, url_prefix='/facebook_xnr_community')

