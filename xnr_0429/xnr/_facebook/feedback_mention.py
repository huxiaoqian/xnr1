#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
import time
from es import Es_fb

class Mention():
	def get_mention(self):
		for url in mention_list:
			driver.get(url)
			for each in driver.find_elements_by_xpath('//div[@id="contentArea"]'):
				author_name = each.find_element_by_xpath('./div/div[3]/div/div/div/div[2]/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div[2]/h5/span/span/a').text
				author_id = ''.join(re.findall(re.compile('id=(\d+)'),each.find_element_by_xpath('./div/div[3]/div/div/div/div[2]/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div[2]/h5/span/span/a').get_attribute('data-hovercard')))
				pic_url = each.find_element_by_xpath('./div/div[3]/div/div/div/div/div/div[2]/div/div/a/div/img').get_attribute('src')
				time = each.find_element_by_xpath('./div/div[3]/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/div/div/div[2]/div/span[3]/span/a/abbr').get_attribute('data-utime')
				try:
					content = each.find_element_by_xpath('./div/div[3]/div/div/div/div[2]/div/div[2]/div[2]/div/div/p').text
				except Exception as e:
					content = 'None'
	def save(self,indexName,typeName,item):
		es.executeES(indexName,typeName,item)

if __name__ == '__main__':
	fb = Launcher('18538728360','zyxing,0513')
	es = es_twitter()
	mention_list = fb.get_mention_list()
	mention = Mention()
	mention.get_mention()
