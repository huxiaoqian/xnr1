# -*-coding:utf-8-*-
import os
import time
import json
import pinyin
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect

mod = Blueprint('weibo_xnr_knowledge_base_management', __name__, url_prefix='/weibo_xnr_knowledge_base_management')
