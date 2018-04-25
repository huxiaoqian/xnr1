#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
import time
from es import Es_fb

class Like():
	def __init__(self):
		self.like_list = Launcher('18538728360','zyxing,0513').get_like_list()

	def get_like(self):
		for url in like_list:
			driver.get(url)
			root_name = driver.find_element_by_xpath('//span[@class="fwb"]').text
			print(root_name)
			id = ''.join(re.findall(re.compile('id=(\d+)'),driver.find_element_by_xpath('//span[@class="fwb"]/a').get_attribute('data-hovercard')))
			print(id)
			try:
				root_content = driver.find_element_by_xpath('//div[@class="_58jw"]/p').text
			except Exception as e:
				root_content = 'None'
			print(root_content)
			driver.get(driver.find_element_by_xpath('//a[@class="_2x4v"]').get_attribute('href'))
			time.sleep(10)
			for each in driver.find_elements_by_xpath('//li[@class="_5i_q"]'):
				author_name = each.find_element_by_xpath('./div/div/div/div[1]/div[2]/div/a').text
				print(author_name)
				author_id = ''.join(re.findall(re.compile('id=(\d+)'),each.find_element_by_xpath('./div/div/div/div[1]/div[2]/div/a').get_attribute('data-hovercard')))
				print(author_id)
				pic_url = each.find_element_by_xpath('./div/a/div/img').get_attribute('src')
				print(pic_url)
				relationship = each.find_element_by_xpath('./div/div/div/div[2]/div[2]/span/div/a/span[2]/span').text
				print(relationship)
			print('-----')
			time.sleep(10)
	
	def save(self,indexName,typeName,item):
		es.executeES(indexName,typeName,item)

if __name__ == '__main__':
	fb = Launcher('18538728360','zyxing,0513')
	es = es_twitter()
	like_list = fb.get_like_list()
	like = Like()
	like.get_like()

	










