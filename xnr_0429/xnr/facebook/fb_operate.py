#!/usr/bin/env python
# encoding: utf-8

import requests
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from lxml import etree
import re
from pybloom import BloomFilter
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from launcher import Launcher

class Operation():
	def __init__(self, username, password):
		print '11'
		self.launcher = Launcher(username, password)
		print '22'

	def publish(self, text):
		driver,display = self.launcher.login()
		try:
			# 退出通知弹窗进入页面
			time.sleep(1)
			try:
				driver.find_element_by_xpath('//div[@class="_n8 _3qx uiLayer _3qw"]').click()
			except:
				pass
			try:
				driver.find_element_by_xpath('//textarea[@title="分享新鲜事"]').click()
				driver.find_element_by_xpath('//textarea[@title="分享新鲜事"]').send_keys(text)
			except:
				try:
					driver.find_element_by_xpath('//textarea[@class="_3en1 _480e navigationFocus"]').click()
					driver.find_element_by_xpath('//textarea[@class="_3en1 _480e navigationFocus"]').send_keys(text)
				except:
					driver.find_element_by_xpath('//div[@class="_1mwp navigationFocus _395 _1mwq _4c_p _5bu_ _34nd _21mu _5yk1"]').click()
					driver.find_element_by_xpath('//div[@class="_1mwp navigationFocus _395 _1mwq _4c_p _5bu_ _34nd _21mu _5yk1"]').send_keys(text)
			try:
				driver.find_element_by_xpath('//button[@class="_1mf7 _4jy0 _4jy3 _4jy1 _51sy selected _42ft"]').click()
			except:
				try:
					driver.find_element_by_xpath('//button[@class="_42ft _4jy0 _ej1 _4jy3 _4jy1 selected _51sy"]').click()
				except:
					driver.find_element_by_xpath('//button[@data-testid="react-composer-post-button"]').click()
			time.sleep(5)
			return [True, '']
		except Exception as e:
			return [False, e]
		finally:
			driver.quit()
			display.popen.kill()

	def mention(self, username, text):
		driver,display = self.launcher.login()
		try:
			# 退出通知弹窗进入页面
			time.sleep(1)
			try:
				driver.find_element_by_xpath('//div[@class="_n8 _3qx uiLayer _3qw"]').click()
			except:
				pass

			try:
				driver.find_element_by_xpath('//textarea[@title="分享新鲜事"]').click()
				driver.find_element_by_xpath('//textarea[@title="分享新鲜事"]').send_keys(text)
			except:
				driver.find_element_by_xpath('//div[@class="_1mwp navigationFocus _395 _1mwq _4c_p _5bu_ _34nd _21mu _5yk1"]').click()
				driver.find_element_by_xpath('//div[@class="_1mwp navigationFocus _395 _1mwq _4c_p _5bu_ _34nd _21mu _5yk1"]').send_keys(text)
			time.sleep(2)
			try:
				driver.find_element_by_xpath('//table[@class="uiGrid _51mz _5f0n"]/tbody/tr[3]/td[1]//a/div').click()
			except:
				driver.find_element_by_xpath('//table[@class="uiGrid _51mz _5f0n"]/tbody/tr[2]/td[2]//a/div').click()
			time.sleep(1)
			driver.find_element_by_xpath('//input[@aria-label="你和谁一起？"]').send_keys(username)
			driver.find_element_by_xpath('//input[@aria-label="你和谁一起？"]').send_keys(Keys.ENTER)
			time.sleep(1)
			try:
				driver.find_element_by_xpath('//button[@class="_1mf7 _4jy0 _4jy3 _4jy1 _51sy selected _42ft"]').click()
			except:
				driver.find_element_by_xpath('//button[@data-testid="react-composer-post-button"]').click()
			time.sleep(5)
			return [True, '']
		except Exception as e:
			return [False, e]
		finally:
			driver.quit()
			display.popen.kill()

	def follow(self, uid):
		try:
			driver,display = self.launcher.target_page(uid)
			# 退出通知弹窗进入页面
			time.sleep(1)
			try:
				driver.find_element_by_xpath('//div[@class="_n8 _3qx uiLayer _3qw"]').click()
			except:
				pass
			try:
				driver.find_element_by_xpath('//button[@data-testid="page_profile_follow_button_test_id"]').click()
			except:
				driver.find_element_by_xpath('//div[@id="pagelet_timeline_profile_actions"]/div[2]/a[1]').click()
			time.sleep(5)
			return [True, '']
		except Exception as e:
			return [False, e]
		finally:
			driver.quit()
			display.popen.kill()

	def not_follow(self, uid):
		try:
			driver,display = self.launcher.target_page(uid)
			# 退出通知弹窗进入页面
			time.sleep(1)
			try:
				driver.find_element_by_xpath('//div[@class="_n8 _3qx uiLayer _3qw"]').click()
			except:
				pass
			chain = ActionChains(driver)
			try:
				implement = driver.find_element_by_xpath('//div[@id="pagelet_timeline_profile_actions"]/div[2]/div[1]/div[1]')
				chain.move_to_element(implement).perform()
				time.sleep(2)
				implement = driver.find_element_by_xpath('//div[@id="pagelet_timeline_profile_actions"]/div[2]/div[1]/div[1]')
				chain.move_to_element(implement).perform()
				time.sleep(2)
				driver.find_element_by_xpath('//a[@ajaxify="/ajax/follow/unfollow_profile.php?profile_id=%s&location=1"]'%uid).click()
			except:
				try:
					implement = driver.find_element_by_xpath('//button[@data-testid="page_profile_follow_button_test_id"]')
					chain.move_to_element(implement).perform()
					time.sleep(2)
					implement = driver.find_element_by_xpath('//button[@data-testid="page_profile_follow_button_test_id"]')
					chain.move_to_element(implement).perform()
					time.sleep(2)
					driver.find_element_by_xpath('//a[@ajaxify="/ajax/follow/unfollow_profile.php?profile_id=%s&location=1"]'%uid).click()
				except:
					implement = driver.find_element_by_xpath('//button[@class="_42ft _4jy0 _3oz- _52-0 _4jy4 _517h _51sy"]')
					chain.move_to_element(implement).perform()
					time.sleep(2)
					implement = driver.find_element_by_xpath('//button[@class="_42ft _4jy0 _3oz- _52-0 _4jy4 _517h _51sy"]')
					chain.move_to_element(implement).perform()
					time.sleep(2)
					driver.find_element_by_xpath('//a[@ajaxify="/ajax/follow/unfollow_profile.php?profile_id=%s&location=1"]'%uid).click()
			time.sleep(5)
			return [True, '']
		except Exception as e:
			return [False, e]
		finally:
			driver.quit()
			display.popen.kill()

# 私信(未关注)
	def send_message(self, uid, text):
		#发送给未关注的用户
		try:
			driver,display = self.launcher.target_page(uid)
			message_url = 'https://www.facebook.com/messages/t/' + uid
			driver.get(message_url)
			time.sleep(5)
			# 退出通知弹窗进入页面
			time.sleep(1)
			try:
				driver.find_element_by_xpath('//div[@class="_n8 _3qx uiLayer _3qw"]').click()
			except:
				pass
			driver.find_element_by_xpath('//div[@aria-label="输入消息..."]').send_keys(text)
			driver.find_element_by_xpath('//div[@aria-label="输入消息..."]').send_keys(Keys.ENTER)
			time.sleep(5)
			return [True, '']
		except Exception as e:
			return [False, e]
		finally:
			driver.quit()
			display.popen.kill()

# 私信(已关注)
	# def send_message2(self, uid, text):
	# 	#发送给已关注的用户
	# 	try:
	# 		driver = self.launcher.target_page(uid)
	# 		url = driver.find_element_by_xpath('//a[@class="_51xa _2yfv _3y89"]/a[1]').get_attribute('href')
	# 		driver.get('https://www.facebook.com' + url)
	# 		time.sleep(4)
	# 		driver.find_element_by_xpath('//div[@class="_1mf _1mj"]').click()
	# 		driver.find_element_by_xpath('//div[@class="_1mf _1mj"]').send_keys(text)
	# 		driver.find_element_by_xpath('//div[@class="_1mf _1mj"]').send_keys(Keys.ENTER)
	# 	finally:
	# 		driver.quit()


# 点赞
	def like(self, uid, fid):
		driver,display = self.launcher.login()
		try:
			post_url = 'https://www.facebook.com/' + uid + '/posts/' + fid
			video_url = 'https://www.facebook.com/' + uid + '/videos/' + fid
			driver.get(post_url)
			time.sleep(3)
			try:
				# 退出通知弹窗进入页面
				time.sleep(1)
				try:
					driver.find_element_by_xpath('//div[@class="_n8 _3qx uiLayer _3qw"]').click()
				except:
					pass
				driver.find_element_by_xpath('//div[@aria-label="Facebook 照片剧场模式"]')
				driver.get(video_url)
				time.sleep(2)
				# 退出通知弹窗进入页面
				time.sleep(1)
				try:
					driver.find_element_by_xpath('//div[@class="_n8 _3qx uiLayer _3qw"]').click()
				except:
					pass
				for each in driver.find_elements_by_xpath('//a[@data-testid="fb-ufi-likelink"]'):
					try:
						each.click()
					except:
						pass
			except:
				# 退出通知弹窗进入页面
				time.sleep(1)
				try:
					driver.find_element_by_xpath('//div[@class="_n8 _3qx uiLayer _3qw"]').click()
				except:
					pass
				for each in driver.find_elements_by_xpath('//a[@data-testid="fb-ufi-likelink"]'):
					try:
						each.click()
					except:
						pass
			time.sleep(5)
			return [True, '']
		except Exception as e:
			return [False, e]
		finally:
			driver.quit()
			display.popen.kill()

# 评论
	def comment(self, uid, fid, text):
		driver,display = self.launcher.login()
		try:
			post_url = 'https://www.facebook.com/' + uid + '/posts/' + fid
			video_url = 'https://www.facebook.com/' + uid + '/videos/' + fid
			driver.get(post_url)
			time.sleep(3)
			try:
				# 退出通知弹窗进入页面
				time.sleep(1)
				try:
					driver.find_element_by_xpath('//div[@class="_n8 _3qx uiLayer _3qw"]').click()
				except:
					pass
				driver.find_element_by_xpath('//div[@aria-label="Facebook 照片剧场模式"]')
				driver.get(video_url)
				# 退出通知弹窗进入页面
				time.sleep(1)
				try:
					driver.find_element_by_xpath('//div[@class="_n8 _3qx uiLayer _3qw"]').click()
				except:
					pass
				time.sleep(3)
				driver.find_element_by_xpath('//div[@class="UFICommentContainer"]/div/div').click()
				time.sleep(1)
				driver.find_element_by_xpath('//div[@class="notranslate _5rpu"]').click()
				time.sleep(1)
				driver.find_element_by_xpath('//div[@class="notranslate _5rpu"]').send_keys(text)
				time.sleep(1)
				driver.find_element_by_xpath('//div[@class="notranslate _5rpu"]').send_keys(keys.ENTER)
			except:
				# 退出通知弹窗进入页面
				time.sleep(1)
				try:
					driver.find_element_by_xpath('//div[@class="_n8 _3qx uiLayer _3qw"]').click()
				except:
					pass
				time.sleep(3)
				driver.find_element_by_xpath('//div[@class="UFICommentContainer"]/div/div').click()
				time.sleep(1)
				driver.find_element_by_xpath('//div[@class="notranslate _5rpu"]').click()
				time.sleep(1)
				driver.find_element_by_xpath('//div[@class="notranslate _5rpu"]').send_keys(text)
				time.sleep(1)
				driver.find_element_by_xpath('//div[@class="notranslate _5rpu"]').send_keys(keys.ENTER)
			time.sleep(5)
			return [True, '']
		except Exception as e:
			return [False, e]
		finally:
			time.sleep(3)
			driver.quit()
			display.popen.kill()

# 分享
	def share(self, uid, fid, text):
		driver,display = self.launcher.login()
		try:
			print 'uid, fid, text...',uid, fid, text
			post_url = 'https://www.facebook.com/' + uid + '/posts/' + fid
			video_url = 'https://www.facebook.com/' + uid + '/videos/' + fid
			driver.get(post_url)
			time.sleep(3)
			try:
				# 退出通知弹窗进入页面
				time.sleep(1)
				try:
					driver.find_element_by_xpath('//div[@class="_n8 _3qx uiLayer _3qw"]').click()
				except:
					pass
				driver.find_element_by_xpath('//div[@aria-label="Facebook 照片剧场模式"]')
				driver.get(video_url)
				time.sleep(1)
				# 退出通知弹窗进入页面
				time.sleep(1)
				try:
					driver.find_element_by_xpath('//div[@class="_n8 _3qx uiLayer _3qw"]').click()
				except:
					pass
				driver.find_element_by_xpath('//a[@title="发送给好友或发布到你的时间线上。"]').click()
				driver.find_element_by_xpath('//a[@title="发送给好友或发布到你的时间线上。"]').click()
				time.sleep(3)
				driver.find_element_by_xpath('//ul[@class="_54nf"]/li[2]').click()
				time.sleep(3)
				try:
					driver.find_element_by_xpath('//div[@class="notranslate _5rpu"]').click()
					time.sleep(1)
					driver.find_element_by_xpath('//div[@class="notranslate _5rpu"]').send_keys(text)
					time.sleep(1)
				except:
					driver.find_element_by_xpath('//div[@class="_1mwp navigationFocus _395  _21mu _5yk1"]/div').click()
					time.sleep(1)
					driver.find_element_by_xpath('//div[@class="_1mwp navigationFocus _395  _21mu _5yk1"]/div').send_keys(text)
					time.sleep(1)
				driver.find_element_by_xpath('//button[@data-testid="react_share_dialog_post_button"]').click()
			except:
				# 退出通知弹窗进入页面
				time.sleep(1)
				try:
					driver.find_element_by_xpath('//div[@class="_n8 _3qx uiLayer _3qw"]').click()
				except:
					pass
				driver.find_element_by_xpath('//a[@title="发送给好友或发布到你的时间线上。"]').click()
				driver.find_element_by_xpath('//a[@title="发送给好友或发布到你的时间线上。"]').click()
				time.sleep(5)
				driver.find_element_by_xpath('//ul[@class="_54nf"]/li[2]').click()
				time.sleep(5)
				try:
					driver.find_element_by_xpath('//div[@class="notranslate _5rpu"]').click()
					time.sleep(1)
					driver.find_element_by_xpath('//div[@class="notranslate _5rpu"]').send_keys(text)
					time.sleep(1)
				except:
					driver.find_element_by_xpath('//div[@class="_1mwp navigationFocus _395  _21mu _5yk1"]/div').click()
					time.sleep(1)
					driver.find_element_by_xpath('//div[@class="_1mwp navigationFocus _395  _21mu _5yk1"]/div').send_keys(text)
					time.sleep(1)
				driver.find_element_by_xpath('//button[@data-testid="react_share_dialog_post_button"]').click()
			time.sleep(5)
			return [True, '']
		except Exception as e:
			return [False, e]
		finally:
			driver.quit()
			display.popen.kill()

#添加好友
	def add_friend(self, uid):
		try:
			driver,display = self.launcher.target_page(uid)
			driver.find_element_by_xpath('//button[@class="_42ft _4jy0 FriendRequestAdd addButton _4jy4 _517h _9c6"]').click()
			time.sleep(5)
			return [True, '']
		except Exception as e:
			return [False, e]
		finally:
			driver.quit()
			display.popen.kill()

#确认好友请求
	def confirm(self, uid):
		try:
			driver,display = self.launcher.target_page(uid)
			time.sleep(5)
			driver.find_element_by_xpath('//div[@class="incomingButton"]/button').click()
			time.sleep(1)
			driver.find_element_by_xpath('//li[@data-label="确认"]/a').click()
			time.sleep(5)
			return [True, '']
		except Exception as e:
			return [False, e]
		finally:
			driver.quit()
			display.popen.kill()

#删除好友
	def delete_friend(self, uid):
		try:
			driver,display = self.launcher.target_page(uid)
			time.sleep(1)
			driver.find_element_by_xpath('//div[@id="pagelet_timeline_profile_actions"]/div/a').click()
			time.sleep(2)
			driver.find_element_by_xpath('//li[@data-label="删除好友"]/a').click()
			time.sleep(5)
			return [True, '']
		except Exception as e:
			return [False, e]
		finally:
			driver.quit()
			display.popen.kill()

if __name__ == '__main__':
	operation = Operation('13041233988','Hanmc0322*')
	#operation = Operation('8618348831412','Z1290605918')
	time.sleep(1)
	list = operation.publish(u'四月十日')
	print(list)
	#operation.mention('xxx','4.9')
	#operation.not_follow('100023080760480')
	#operation.send_message('100023080760480', 'hello')
	#operation.like('183774741715570','1487409108018787')
	#operation.comment('100012258524129','418205591931388','emmmm')
	#operation.share('183774741715570','1487409108018787','emmmm')
	#operation.add_friend('183774741715570')
