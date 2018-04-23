#!/usr/bin/env python
#encoding: utf-8

from launcher import Launcher
import time
from es import Es_fb

class Share():
	def get_share(self):
		driver.get(share_list[0])
		for ea in driver.find_elements_by_xpath('//div[@id="repost_view_permalink"]/div/div[1]/div'):
			for each in ea.find_elements_by_xpath('./div'):
				print(each.get_attribute('id'))
				author_name = each.find_element_by_xpath('./div/div[2]/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div[2]/h5/span/span/span/a').text
				print(author_name)
				author_id = re.findall(re.compile('id=(\d+)'),each.find_element_by_xpath('./div/div[2]/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div[2]/h5/span/span/span/a').get_attribute('data-hovercard'))
				pic_url = each.find_element_by_xpath('./div/div[2]/div/div[2]/div/div/a/div/img').get_attribute('src')
				try:
					content = each.find_element_by_xpath('./div/div[2]/div/div[2]/div[2]//p').text
				except Exception as e:
					content = 'None'
				time = each.find_element_by_xpath('./div/div[2]/div/div[2]/div/div/div/div[2]/div/div/div[2]/div/span[3]/span/a/abbr').get_attribute('data-utime')
				root_url = 'https://www.facebook.com/'+each.find_element_by_xpath('./div/div[2]/div/div[2]/div/div/div/div[2]/div/div/div[2]/h5/span/span/a').get_attribute('href')

	def save(self,indexName,typeName,item):
		es.executeES(indexName,typeName,item)

if __name__ == '__main__':
	fb = Launcher('18538728360','zyxing,0513')
	es = es_twitter()
	share_list = fb.get_share_list()
	share = Share()
	share.get_share()
