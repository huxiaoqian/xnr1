#!/usr/bin/env python
#encoding: utf-8

from selenium import webdriver
import requests
import time
from pyvirtualdisplay import Display
from launcher import Launcher
from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
import sys
sys.path.append('../')
from timed_python_files import new_facebook_xnr_flow_text_mappings as mapping

display = Display(visible=0, size=(1024,768))
display.start()

# 获取已创建xnr的数据
es = Elasticsearch([{'host':'219.224.134.213','port':9205}])
xnrData = []
query_body = {
		"query":
		{
			"match": {
				"create_status": 2
			}
		}
}
res = es.search(index='fb_xnr', doc_type='user', body=query_body, request_timeout=100)
hits = res['hits']['hits']
for each in hits:
	if each['_source']['create_status'] == 2:
		xnrData.append(each['_source'])

for xnr in xnrData:
	xnr_user_no = xnr['xnr_user_no']
	uid = xnr['uid']
	account = xnr['fb_mail_account']
	password = xnr['password']
	# 登录
	driver = webdriver.Firefox()
	driver.get('https://www.facebook.com')
	driver.find_element_by_xpath('//input[@id="email"]').send_keys(account)
	driver.find_element_by_xpath('//input[@id="pass"]').send_keys(password)
	driver.find_element_by_xpath('//input[@data-testid="royal_login_button"]').click()
	time.sleep(2)
	# 退出通知弹窗进入页面
	try:
		driver.find_element_by_xpath('//div[@class="_n8 _3qx uiLayer _3qw"]').click()
	except:
		pass
	time.sleep(1)
	# 点掉进入主页之后的提醒
	try:
		driver.find_element_by_xpath('//a[@action="cancel"]').click()
	except Exception as e:
		pass
	time.sleep(1)



















