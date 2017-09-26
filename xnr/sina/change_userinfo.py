#-*- coding: utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.support.select import Select

def change_userinfo(uname, pwd, profile_info_dict):
    #step1: login
    driver = webdriver.Firefox(executable_path='geckodriver')
    url = 'http://www.weibo.com/login.php'
    driver.get(url)
    driver.find_element_by_xpath('//*[@id="loginname"]').send_keys(uname)
    time.sleep(1)
    driver.find_element_by_name('password').send_keys(pwd)
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click()
    time.sleep(1)
    #step2: profile url
    profile_url = 'http://www.weibo.com/p/100505'+uid+'/info?mod=pedit'
    driver.get(profile_url)
    time.sleep(1)
    #step3: edit profile information
    profile_url_2 = 'http://account.weibo.com/set/iframe?skin=skin048'
    driver.get(profile_url_2)
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="pl_content_account"]/div[1]/form/fieldset/div/a').click()
    time.sleep(1)
    #step3.1: edit location
    edit_province = driver.find_element_by_xpath('//*[@id="province"]')
    province_select = Select(edit_province)
    province_select.select_by_visible_text(profile_info_dict['location_province'])
    time.sleep(1)
    edit_city = driver.find_element_by_xpath('//*[@id="city"]')
    city_select = Select(edit_city)
    city_select.select_by_visible_text(profile_info_dict['location_city'])
    time.sleep(1)
    #step3.2: male/female
    if profile_info_dict['gender'] == 'man':
        driver.find_element_by_id('man_radio').click()
    else:
        driver.find_element_by_id('woman_radio').click()
    time.sleep(1)
    #step3.3: description
    driver.find_element_by_xpath('//*[@id="pl_content_account"]/div[1]/div[2]/div/div[12]/div[2]/textarea').clear()
    driver.find_element_by_xpath('//*[@id="pl_content_account"]/div[1]/div[2]/div/div[12]/div[2]/textarea').send_keyssend_keys(profile_info_dict['description'])
    time.sleep(1)
    #step3.4: birth
    edit_year = driver.find_element_by_xpath('//*[@id="pl_content_account"]/div[1]/div[2]/div/div[9]/div[3]/div/select[1]')
    year_select = Select(edit_year)
    year_select.select_by_visible_text(profile_info_dict['birth'][0])
    time.sleep(1)
    edit_month = driver.find_element_by_xpath('//*[@id="pl_content_account"]/div[1]/div[2]/div/div[9]/div[3]/div/select[2]')
    month_select = Select(edit_month)
    month_select.select_by_visible_text(profile_info_dict['birth'][1])
    time.sleep(1)
    edit_day = driver.find_element_by_xpath('//*[@id="pl_content_account"]/div[1]/div[2]/div/div[9]/div[3]/div/select[3]')
    day_select = Select(edit_day)
    day_select.select_by_visible_text(profile_info_dict['bisth'][2])
    time.sleep(1)
    #step4: save
    driver.find_element_by_xpath('//*[@id="pl_content_account"]/div[1]/form/fieldset/div/a').click()
    time.sleep(2)
    #close
    driver.close()

if __name__=='__main__':
    #change user info
    uname = 'weiboxnr04@126.com'
    pwd = 'xnr123456'
    uid = '6346321407'
    profile_info_dict = {'description': 'aaaa', 'location_province':'黑龙江',\
            'location_city':'大庆','gender': 'man',\
            'birth':['1985', '08', '06']}
    change_userinfo(uname, pwd, userinfo_dict)
