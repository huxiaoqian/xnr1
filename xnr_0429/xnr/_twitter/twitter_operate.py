#!/usr/bin/env python
# encoding: utf-8

from selenium import webdriver
import requests
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from lxml import etree
import re
from pybloom import BloomFilter
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import *
import tweepy
from tweepy import OAuthHandler
from elasticsearch import Elasticsearch

from launcher import Launcher
from es import Es_twitter

# elasticsearch
#es = es_twitter()

#driver = Launcher('18538728360@163.com','zyxing,0513').login()
#api = Launcher('18538728360@163.com','zyxing,0513').api()

class Operation():
	def __init__(self):
		pass

	def publish(self,text):
		api = Launcher('18538728360@163.com','zyxing,0513').api()
		api.update_status(text)

	def mention(self,text):
		#text = '@lvleilei1 test'
		api = Launcher('18538728360@163.com','zyxing,0513').api()
		api.update_status(text)

	def message(self):
		api = Launcher('18538728360@163.com','zyxing,0513').api()
		api.send_direct_message('lvleilei1',text='test send direct message')

	def follow(self,screen_name):
		api = Launcher('18538728360@163.com','zyxing,0513').api()
		api.create_friendship(screen_name)

	def destroy_friendship(self,screen_name):
		api = Launcher('18538728360@163.com','zyxing,0513').api()
		api.destroy_friendship(screen_name)







