#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
from es import Es_twitter

class Userinfo():
	def __init__(self, username, password):
		self.launcher = Launcher(username, password)
		
	def login(self):
		try:
			self.driver = self.launcher.login()
			screen_name = self.driver.find_element_by_xpath('//b[@class="u-linkComplex-target"]').text
			return screen_name
		except Exception as e:
			print(e)

	def getUserinfo(self):
		screen_name = self.login()
		uid = self.launcher.get_user(screen_name).id
		description = self.launcher.get_user(screen_name).description
		lcoation = self.launcher.get_user(screen_name).location
		dict = {'uid':uid,'desccription':description,'location':location}
		return dict