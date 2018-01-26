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
		self.api = self.launcher.api()
		self.list = []

	def publish(self, text):
		try:
			self.api.update_status(text)
		except Exception as e:
			print(e)


	#API.update_with_media(filename[, status][, in_reply_to_status_id][, auto_populate_reply_metadata][, lat][, long][, source][, place_id][, file])
	def publish_with_media(self, filename, text):
		try:
			self.api.update_with_media(filename, text)
		except Exception as e:
			print(e)

	def mention(self, text):
		#text = '@lvleilei1 test'
		try:
			self.api.update_status(text)
		except Exception as e:
			print(e)

	def message(self, uid, text):
		try:
			print self.api.send_direct_message(uid, text=text)
		except Exception as e:
		 	print(e)

	def follow(self, uid):
		try:
			self.api.create_friendship(uid)
		except Exception as e:
			print(e)

	def destroy_friendship(self, uid):
		try:
			self.api.destroy_friendship(uid)
		except Exception as e:
			print(e)

	def do_retweet(self, tid):
		try:
			self.api.retweet(tid)
		except Exception as e:
		 	print(e)

	def do_retweet_text(self, uid, tid, text):
		try:
			driver = self.launcher.login()
			screen_name = self.launcher.get_user(uid)
			post_url = 'https://twitter.com/' + screen_name + '/status/' + tid
			driver.get(post_url)
			time.sleep(3)
			current_url = driver.current_url
			pattern = re.compile('status/(\d+)')
			primary_id = ''.join(re.findall(pattern,current_url)).strip()
			driver.find_element_by_xpath('//button[@aria-describedby="profile-tweet-action-retweet-count-aria-%s"]'%primary_id).click()
			time.sleep(3)
			driver.find_element_by_xpath('//div[@id="retweet-with-comment"]').click()
			driver.find_element_by_xpath('//div[@id="retweet-with-comment"]').send_keys(text)
			driver.find_element_by_xpath('//button[@class="EdgeButton EdgeButton--primary retweet-action"]').click()
		except Exception as e:
			print(e)

	def do_favourite(self, tid):
		try:
			self.api.create_favorite(tid)
		except Exception as e:
			print(e)

	def do_comment(self, uid, tid, text):
		try:
			driver = self.launcher.login()
			screen_name = self.launcher.get_user(uid)
			post_url = 'https://twitter.com/' + screen_name + '/status/' + tid
			driver.get(post_url)
			time.sleep(1)
			current_url = driver.current_url
			pattern = re.compile('status/(\d+)')
			primary_id = ''.join(re.findall(pattern,current_url)).strip()
			driver.find_element_by_xpath('//div[@id="tweet-box-reply-to-%s"]'%primary_id).click()
			driver.find_element_by_xpath('//div[@id="tweet-box-reply-to-%s"]'%primary_id).send_keys(text)
			time.sleep(1)
			driver.find_element_by_xpath('//button[@class="tweet-action EdgeButton EdgeButton--primary js-tweet-btn"]').click()
		except Exception as e:
			print(e)



if __name__ == '__main__':
	operation = Operation('8617078448226','xnr123456')
	#operation.publish('12.26 test')
	#operation.message('lvleilei1',text='test')
	#operation.do_comment('871936760573382658','922897194100826112','.....')
	operation.do_retweet_text('348484872','922898277774843904','emmmm')



