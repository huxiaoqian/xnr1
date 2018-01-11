#!/usr/bin/env python
#encoding: utf-8

from selenium import webdriver
import tweepy
from tweepy import OAuthHandler
import requests
import time

class Launcher():
	def __init__(self,username,password):
		self.username = username
		self.password = password
		self.consumer_key = 'v87gW3XqF49PL13xRYGsdVTXX'
		self.consumer_secret = 'Bzm94HKmBwkbwlCsPsAwv3wU2PYbuGPO6IfZ4TiaR4bZOBEvMR'
		self.access_token = '943290911039029250-ZKg5KT0edFDGctuVbHvWCJWoZ9CmV5t'
		self.access_secret = 'OEcFiPfqUihKUzW61ZR23fOkMY5BIsDRjj5urf8rmYMTt'

	def login(self):
		driver = webdriver.Firefox()
		driver.get('https://twitter.com/login')
		time.sleep(3)
		driver.find_element_by_xpath('//input[@class="js-username-field email-input js-initial-focus"]').send_keys(self.username)
		driver.find_element_by_xpath('//input[@class="js-password-field"]').click()
		driver.find_element_by_xpath('//input[@class="js-password-field"]').send_keys(self.password)
		driver.find_element_by_xpath('//button[@class="submit EdgeButton EdgeButton--primary EdgeButtom--medium"]').click()
		time.sleep(1)
		req = requests.Session()
		cookies = driver.get_cookies()
		for cookie in cookies:
			req.cookies.set(cookie['name'],cookie['value'])
		headers = {
			'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:56.0) Gecko/20100101 Firefox/56.0'
		}
		return driver

	def api(self):
		auth = OAuthHandler(self.consumer_key,self.consumer_secret)
		auth.set_access_token(self.access_token,self.access_secret)
		api = tweepy.API(auth)
		return api

	def get_user(self, uid):
		api = self.api()
		screen_name = api.get_user(uid).screen_name
		return screen_name

if __name__ == '__main__':
	launcher = Launcher('18538728360@163.com','zyxing,0513')
	driver = launcher.login()
	api = launcher.api()





