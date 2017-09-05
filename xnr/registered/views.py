#-*- coding:utf-8 -*-
import os
import time
import json
import pinyin
from flask import Blueprint, url_for, render_template, request,\
                  abort, flash, session, redirect
mod = Blueprint('registered', __name__, url_prefix='/registered')

@mod.route('/targetCustom/')
def targetCustom():
    return render_template('registered/target_custom.html')

@mod.route('/virtualCreated/')
def virtualCreated():
    continueUser = request.args.get('continueUser','')
    domainName = request.args.get('domainName','')
    roleName = request.args.get('roleName','')
    daily = request.args.get('daily', '')
    psyFeature = request.args.get('psyFeature','')
    politicalSide = request.args.get('politicalSide', '')
    businessGoal = request.args.get('businessGoal', '')
    monitorKeywords = request.args.get('monitorKeywords', '')
    return render_template('registered/virtual_created.html',continueUser=continueUser,domainName=domainName,roleName=roleName,
        daily=daily,psyFeature=psyFeature,politicalSide=politicalSide,businessGoal=businessGoal,monitorKeywords=monitorKeywords)
    
@mod.route('/socialAccounts/')
def socialAccounts():
    return render_template('registered/social_accounts.html')

