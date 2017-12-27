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

class Operation():
	def __init__(self, username, password):
		self.launcher = Launcher(username, password)
		self.driver = self.launcher.login()
		self.api = self.launcher.api()

	def publish(self, text):
		self.api.update_status(text)

	def mention(self, text):
		#text = '@lvleilei1 test'
		self.api.update_status(text)

	def message(self, screen_name, text):
		self.api.send_direct_message(screen_name, text=text)

	def follow(self,screen_name):
		self.api.create_friendship(screen_name)

	def destroy_friendship(self,screen_name):
		self.api.destroy_friendship(screen_name)


if __name__ == '__main__':
	operation = Operation('18538728360@163.com','zyxing,0513')
	#operation.publish('12.26 test')
	#operation.message('lvleilei1',text='test')




