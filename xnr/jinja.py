# -*- coding: utf-8 -*-

from datetime import date


def gender(g):
	if g == 1:
		return u'/../../static/img/male.png'
	elif g == 2:
		return u'/../../static/img/female.png'
	else:
		return u''

def gender_text(g):
	if g == 1:
		return u'男'
	elif g == 2:
		return u'女'
	else:
		return u'未知'
def user_email(g):
	if g == '':
		return u'未知'
	else:
		return g

def user_location(g):
	if g == '':
		return u'未知'
	else:
		return g

def user_birth(g):
	if g == '':
		return u'未知'
	else:
		return g

def user_vertify(g):
	if g == 0:
		return u'未认证'
	elif g == 1:
		return u'已认证'
	else:
		return u'未知'

def weibo_source(g):
	if g == 1:
		return u'新浪'
	elif g == 2:
		return u'腾讯'
	elif g == 3:
		return u'搜狐'
	elif g == 4:
		return u'网易'
	else:
		return u'未知'

def Int2string(g):
	return str(g) 


def tsfmt(ts):
    return date.fromtimestamp(ts) if ts else None
