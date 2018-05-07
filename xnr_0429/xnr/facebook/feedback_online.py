#!/usr/bin/env python
#encoding: utf-8

from Elasticsearch_fb import Es_fb
from launcher import Launcher

class Online():
	def __init__(self,username, password):
		self.launcher = Launcher(username, password)
		self.driver = self.launcher.login()

	def get_online(self):
		try:
			name_list = []
			status_list = []
			for each in self.driver.find_elements_by_xpath('//li[@class="_42fz"]/a/div/div[3]'):
				name_list.append(each.text)
			for each in self.driver.find_elements_by_xpath('//li[@class="_42fz"]/a/div/div[2]'):
				try:
					each.find_element_by_xpath('./div/span')
					status = 'online'
					status_list.append(status)
				except Exception as e:
					status = 'None'
					status_list.append(status)
			z = zip(name_list,status_list)
			dict = dict({name,status} for name,status in z)
			print(dict)
		finally:
			self.driver.quit()
			self.launcher.display.popen.kill()

if __name__ == '__main__':
	online = Online('8617078448226','xnr123456')