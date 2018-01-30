#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
from es import Es_twitter
import time
import re

class Userinfo():
	def __init__(self, username, password):
		self.launcher = Launcher(username, password)

	def getUserinfo(self):
		driver = self.launcher.login()
		time.sleep(2)
		driver.find_element_by_xpath('//a[@data-component-context="home_nav"]').click()
		time.sleep(2)
		screen_name_url = driver.find_element_by_xpath('//div[@class="DashboardProfileCard-content"]//a').get_attribute('href')
		driver.get(screen_name_url)
		api = self.launcher.api()
		time.sleep(1)
		screen_name = driver.find_element_by_xpath('//div[@class="ProfileHeaderCard"]/h2//b').text
		uid = api.get_user(screen_name).id
		try:
			description = api.get_user(screen_name).description
		except:
			description = None
		try:
			location = api.get_user(screen_name).location
		except:
			location = None
		today = int(time.strftime('%Y',time.localtime(int(time.time()))))
		try:
			birth = driver.find_element_by_xpath('//span[@class="ProfileHeaderCard-birthdateText u-dir"]/span').text
		except:
			birth = False
		pattern = re.compile(u'(\d+)年')
		pattern1 = re.compile(', (\d+)')
		if birth:
			try:
				birthday = int(re.findall(pattern,birth)[0])
			except:
				birthday = int(re.findall(pattern1,birth)[0])
			age = today - birthday
		else:
			age = None
		dict = {'uid':uid,'desccription':description,'location':location,'age':age}
		print(dict)
		return dict
		
if __name__ == '__main__':
	#userinfo = Userinfo('8617078448226','xnr123456')
	userinfo = Userinfo('feifanhanmc@163.com', 'han8528520258')
	userinfo.getUserinfo()