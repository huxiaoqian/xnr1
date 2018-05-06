#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
import time
import re

class Userinfo:
	def __init__(self, username, password):
		self.launcher = Launcher(username, password)

	def getUserinfo(self):
		driver = self.launcher.login()
		time.sleep(2)
		driver.find_element_by_xpath('//a[@title="个人主页"]').click()
		time.sleep(1)
		driver.find_element_by_xpath('//a[@data-tab-key="about"]').click()
		time.sleep(1)

		current_url = driver.current_url
		pattern0 = re.compile('id=(\d+)')
		id = re.findall(pattern0, current_url)[0]

		eachs = [each for each in driver.find_elements_by_xpath('//div[@data-pnref="overview"]//li')]
		career = eachs[0].text
		location = eachs[2].text
		pattern = re.compile(u'(\d+)年')
		print(eachs[5].text)
		birth = int(re.findall(pattern,eachs[5].text)[0])
		today = int(time.strftime('%Y',time.localtime(int(time.time()))))
		age = today - birth

		driver.find_element_by_xpath('//ul[@data-testid="info_section_left_nav"]/li[6]/a').click()
		time.sleep(1)
		description = driver.find_element_by_xpath('//div[@id="pagelet_bio"]/div/ul/li').text

		dict = {'id':id,'career':career,'location':location,'age':age,'description':description}
		driver.quit()
		display.stop()
		return dict

if __name__ == '__main__':
	#userinfo = Userinfo('8618348831412','Z1290605918')
	userinfo = Userinfo('feifanhanmc@163.com','han8528520258')
	userinfo.getUserinfo()