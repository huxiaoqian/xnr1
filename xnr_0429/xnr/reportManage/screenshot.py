#!/usr/bin/env python
#encoding: utf-8

from selenium import webdriver
import time
from pyvirtualdisplay import Display
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Screen():
	def __init__(self, username, password):
		self.ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
		self.username = username
		self.password = password
		self.login_url = 'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F%3Fjumpfrom%3Dwapv4%26tip%3D1'
		self.display = Display(visible=0,size=(1024,768))
		self.display.start()
		self.driver = webdriver.Firefox()

	def login(self):
		#driver = webdriver.Firefox()
		driver.get(self.login_url)
		time.sleep(1)
		driver.find_element_by_xpath('//input[@id="loginName"]').send_keys(self.username)
		driver.find_element_by_xpath('//input[@id="loginPassword"]').send_keys(self.password)
		driver.find_element_by_xpath('//a[@id="loginAction"]').click()
		time.sleep(5)
		return driver

	def mid_to_url(self, midint):
		result = []
		midint = str(midint)[::-1]
		size = len(midint) / 7 if len(midint) % 7 == 0 else len(midint) / 7 + 1
		size = int(size)
		for i in range(size):
			s = midint[i * 7: (i + 1) * 7][::-1]
			s = self.base62_encode(int(s), self.ALPHABET)
			s_len = len(s)
			if i < size - 1 and len(s) < 4:
				s = '0' * (4 - s_len) + s
			result.append(s)
		result.reverse()
		return ''.join(result)

	def base62_encode(self, num, alphabet):
		if (num == 0):
			return alphabet[0]
		arr = []
		base = len(alphabet)
		while num:
			rem = num % base
			num = num // base
			arr.append(alphabet[rem])
		arr.reverse()
		return ''.join(arr)

	def screenShot(self, uid, mid):
		_mid = self.mid_to_url(mid)
		url = "http://weibo.com/" + uid + "/" + _mid
		print(url)
		self.driver.get(url)
		time.sleep(10)
		print(self.driver.page_source)
		#while True:
		#	try:
		time.sleep(3)
		self.driver.find_element_by_xpath('//div[@node-type="root_child_comment_build"]').screenshot(mid+'.png')
		self.driver.quit()
		self.display.popen.kill()
		#		break
		#	except:
		#		continue














