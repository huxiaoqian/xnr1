# -*-coding=utf-8 -*- 

from selenium import webdriver
from pyvirtualdisplay import Display
import time

display = Display(visible=0, size=(1024, 768))
display.start()
driver = webdriver.Firefox()

def getAppInfo(username, password, app_name, description, url):
	# 登录
	driver.get('https://twitter.com/login')
	time.sleep(3)
	driver.find_element_by_xpath('//input[@class="js-username-field email-input js-initial-focus"]').send_keys(username)
	driver.find_element_by_xpath('//input[@class="js-password-field"]').click()
	driver.find_element_by_xpath('//input[@class="js-password-field"]').send_keys(password)
	driver.find_element_by_xpath('//button[@class="submit EdgeButton EdgeButton--primary EdgeButtom--medium"]').click()

	# 创建第一步
	appUrl = 'https://apps.twitter.com/app/new'
	driver.get(appUrl)
	time.sleep(2)
	while True:
		driver.find_element_by_xpath('//input[@id="edit-name"]').send_keys(app_name)
		driver.find_element_by_xpath('//input[@id="edit-description"]').send_keys(description)
		driver.find_element_by_xpath('//input[@id="edit-url"]').send_keys(url)
		driver.find_element_by_xpath('//input[@id="edit-tos-agreement"]').click()
		driver.find_element_by_xpath('//input[@id="edit-submit"]').click()
		# 是否创建失败
		try:
			error = driver.find_element_by_xpath('//div[@class="alert alert-error"]').text
			print(error)
		except:
			break

	# 修改权限
	currentUrl = driver.current_url
	driver.get(currentUrl + '/permissions')
	driver.find_element_by_xpath('//input[@id="edit-access-level-2"]').click()
	driver.find_element_by_xpath('//input[@id="edit-submit"]').click()

	# 创建第二步
	driver.get(currentUrl + '/keys')
	driver.find_element_by_xpath('//input[@id="edit-submit-owner-token"]').click()

	# 获取
	consumer_key = driver.find_element_by_xpath('//div[@class="app-settings"]/div[1]/span[2]').text
	consumer_secret = driver.find_element_by_xpath('//div[@class="app-settings"]/div[2]/span[2]').text
	access_token = driver.find_element_by_xpath('//div[@class="access"]/div[1]/span[2]').text
	access_secret = driver.find_element_by_xpath('//div[@class="access"]/div[2]/span[2]').text

	return {"consumer_key":consumer_key, "consumer_secret":consumer_secret, "access_token":access_token, "access_secret":access_secret}







