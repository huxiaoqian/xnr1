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
		self.consumer_key = 'IajAzCcakYnbGOkJ90Yv2uFOh'
		self.consumer_secret = 'VLCgFUCMsgsMEJ6zF3laSjsscbgNYWWCxaFhcGzzuol27ocDhI'
		self.access_token = '922372762651561984-7rMZRMQZEoI4lgiZDQnQbJr0dm5msSc'
		self.access_secret = 'pfbceEGlDGcQOhsaBGV3YSnCIsmGPwhJJrjnd0cI1DvD7'
		#self.firefoxProfile = webdriver.FirefoxProfile()
		#self.firefoxProfile.set_preference('permissions.default.stylesheet',2)
		#self.firefoxProfile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so','false')
		#self.firefoxProfile.set_preference('permissions.default.image',2)
		#self.driver = webdriver.Firefox(firefox_profile=self.firefoxProfile)
		self.driver = webdriver.Firefox()
		
	def login(self):
		self.driver.get('https://twitter.com/login')
		time.sleep(3)
		self.driver.find_element_by_xpath('//input[@class="js-username-field email-input js-initial-focus"]').send_keys(self.username)
		self.driver.find_element_by_xpath('//input[@class="js-password-field"]').click()
		#self.driver.find_element_by_xpath('//input[@class="js-password-field"]').send_keys(self.password)
		self.driver.find_element_by_xpath('//input[@class="js-password-field"]').send_keys(self.password)
		self.driver.find_element_by_xpath('//button[@class="submit EdgeButton EdgeButton--primary EdgeButtom--medium"]').click()
		time.sleep(1)
		req = requests.Session()
		cookies = self.driver.get_cookies()
		for cookie in cookies:
			req.cookies.set(cookie['name'],cookie['value'])
		headers = {
			'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:56.0) Gecko/20100101 Firefox/56.0'
		}
		return self.driver

	def api(self):
		auth = OAuthHandler(self.consumer_key,self.consumer_secret)
		auth.set_access_token(self.access_token,self.access_secret)
		api = tweepy.API(auth)
		return api


if __name__ == '__main__':
	launcher = Launcher('18538728360@163.com','zyxing,0513')
	driver = launcher.login()
	api = launcher.api()





