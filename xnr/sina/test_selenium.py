#-*- coding: utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.support.select import Select

def login():
    #step0: set parameter
    uname = 'weiboxnr04@126.com'
    pwd = 'xnr123456'
    uid = '6346321407'
    profile_info_dict = {'description': 'aaaa', 'location_province':'黑龙江',\
            'location_city':'大庆','nick_name':'myname', 'gender': 'man'}
    #?attention: nick name may cannot be changed
    #step1: login
    driver = webdriver.Firefox(executable_path='geckodriver')
    #driver.maximize_window()
    url = 'http://www.weibo.com/login.php'
    driver.get(url)
    #driver.find_element_by_xpath("//*[@id='loginname']").clear()
    driver.find_element_by_xpath('//*[@id="loginname"]').send_keys(uname)
    time.sleep(5)
    driver.find_element_by_name('password').send_keys(pwd)
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click()
    time.sleep(5)
    #driver.get_screenshot_as_file('/home/ubuntu4/huxiaoqian/test_selenium/a.png')
   
    
    profile_url = 'http://www.weibo.com/p/100505'+uid+'/info?mod=pedit'
    #step2: find profile url
    driver.get(profile_url)
    time.sleep(5)
    #step3: edit profile infomation
    profile_url_2 = 'http://account.weibo.com/set/iframe?skin=skin048'
    driver.get(profile_url_2)
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="pl_content_account"]/div[1]/form/fieldset/div/a').click()
    #edit_href_list = driver.find_element_by_class_name("W_btn_round")
    #edit_href = edit_href_list[0]
    #edit_href.click()
    time.sleep(5)
    #edit nick name
    #driver.find_element_by_xpath('//*[@id="pl_content_account"]/div[1]/div[2]/div/div[2]/div[2]/input').clear()
    #driver.find_element_by_xpath('//*[@id="pl_content_account"]/div[1]/div[2]/div/div[2]/div[2]/input').send_keys(profile_info_dict['nick_name'])
    time.sleep(5)
    #edit description
    driver.find_element_by_xpath('//*[@id="pl_content_account"]/div[1]/div[2]/div/div[12]/div[2]/textarea').clear()
    driver.find_element_by_xpath('//*[@id="pl_content_account"]/div[1]/div[2]/div/div[12]/div[2]/textarea').send_keys(profile_info_dict['description'])
    #edit male/female
    if profile_info_dict['gender'] == 'man':
        driver.find_element_by_id('man_radio').click()
    else:
        driver.find_element_by_id('woman_radio').click()
    time.sleep(5)
    #edit location
    #driver.find_element_by_xpath('//*[@id="province"]').select_by_visible_text(profile_info_dict['location_province'])
    edit_province = driver.find_element_by_xpath('//*[@id="province"]')
    province_select = Select(edit_province)
    province_select.select_by_visible_text(profile_info_dict['location_province'])
    time.sleep(5)
    #driver.find_element_by_xpath('//*[@id="city"]').select_by_visible_text(profile_info_dict['location_city'])
    edit_city = driver.find_element_by_xpath('//*[@id="city"]')
    city_select = Select(edit_city)
    city_select.select_by_visible_text(profile_info_dict['location_city'])
    time.sleep(5)
    #click save
    driver.find_element_by_xpath('//*[@id="pl_content_account"]/div[1]/form/fieldset/div/a').click()
    time.sleep(5)
    driver.close()



if __name__=='__main__':
    login()
