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
		self.list = []

	def publish(self, text):
		self.api.update_status(text)

	#API.update_with_media(filename[, status][, in_reply_to_status_id][, auto_populate_reply_metadata][, lat][, long][, source][, place_id][, file])
	def publish_with_media(self, filename, text):
		self.api.update_with_media(filename, text)

	def mention(self, text):
		#text = '@lvleilei1 test'
		self.api.update_status(text)

	def message(self, screen_name, text):
		self.api.send_direct_message(screen_name, text=text)

	def follow(self,screen_name):
		self.api.create_friendship(screen_name)

	def destroy_friendship(self,screen_name):
		self.api.destroy_friendship(screen_name)

	def do_retweet(self, id):
		self.api.retweet(id)

	def do_favourite(self, id):
		self.api.create_favorite(id)

	#评论前要运行target
	def do_comment(self, id):
		self.driver.find_element_by_xpath('//li[@data-item-id="%s"]/div/div[2]/div[4]/div[2]/div[1]/button/div'%id).click()
		time.sleep(10)
		self.driver.find_element_by_xpath('//div[@class="tweet-box rich-editor is-showPlaceholder"]').click()
		self.driver.find_element_by_xpath('//div[@class="tweet-box rich-editor is-showPlaceholder"]').send_keys('11.22 test')
		time.sleep(10)
		self.driver.find_element_by_xpath('//button[@class="tweet-action EdgeButton EdgeButton--primary js-tweet-btn"]').click()

	def target(self, screen_name):
		self.driver.find_element_by_xpath('//input[@id="search-query"]').send_keys(screen_name)
		self.driver.find_element_by_xpath('//input[@id="search-query"]').send_keys(Keys.ENTER)
		time.sleep(10)
		self.driver.find_element_by_xpath('//ul[@class="AdaptiveFiltersBar-nav"]/li[3]/a').click()
		time.sleep(10)
		self.driver.find_element_by_xpath('//div[@class="Grid Grid--withGutter"]/div[1]/div/div/a').click()
		time.sleep(10)
		self.driver.find_element_by_xpath('//a[@data-nav="tweets_with_replies_toggle"]').click()
		time.sleep(10)

	def id(self, screen_name):
		for each in self.api.user_timeline(screen_name):
			id = each.id
			text = each.text
			self.list.append({'id':id,'text':text})
		return self.list



if __name__ == '__main__':
	operation = Operation('18538728360@163.com','zyxing,0513')
	#operation.publish('12.26 test')
	#operation.message('lvleilei1',text='test')




