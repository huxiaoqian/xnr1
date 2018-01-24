#!/usr/bin/env python
#encoding: utf-8

from selenium import webdriver
import tweepy
from tweepy import OAuthHandler
import requests
import time
from pyvirtualdisplay import Display

class Launcher():
	def __init__(self,username,password):
		self.username = username
		self.password = password
		self.consumer_key = 'N1Z4pYYHqwcy9JI0N8quoxIc1'
		self.consumer_secret = 'VKzMcdUEq74K7nugSSuZBHMWt8dzQqSLNcmDmpGXGdkH6rt7j2'
		self.access_token = '943290911039029250-yWtATgV0BLE6E42PknyCH5lQLB7i4lr'
		self.access_secret = 'KqNwtbK79hK95l4X37z9tIswNZSr6HKMSchEsPZ8eMxA9'
		self.display = Display(visible=0,size=(1024,768))
		self.display.start()
	def login(self):
		#driver = webdriver.Firefox()
		driver = webdriver.Chrome()
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
	launcher = Launcher('8617078448226','xnr123456')
	driver = launcher.login()
	api = launcher.api()





