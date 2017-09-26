#-*- coding:utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.support.select import Select

def get_userinfo(uname, pwd):
    #step1: login
    driver = webdriver.Firefox(executable_path='geckodriver')
    url = 'http://www.weibo.com/login.php'
    driver.get(url)
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="loginname"]').send_keys(uname)
    time.sleep(1)
    driver.find_element_by_name('password').send_keys(pwd)
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click()
    time.sleep(7)
    print 'get current url'
    #step1.5: get nick name
    #nick_name_str = driver.find_element_by_xpath('//*[@id="v6_pl_rightmod_myinfo"]/div/div/div[2]/div/a[1]')
    #nick_name_str = driver.find_element_by_xpath('//*[@id="plc_top"]/div/div/div[3]/div[1]/ul/li[5]/a/em[2]')
    #nick_name = nick_name_str.text
    #print 'step1.5 nick_name:', nick_name
    now_url = driver.current_url
    #print 'now_url:', now_url
    url_list = now_url.split('/')
    #print 'url_list:', url_list
    try:
        uid = url_list[4]
    except:
        time.sleep(5)
        now_url = driver.current_url
        uid = now_url.split('/')[4]
    #print 'uid:', uid
    #step2: profile url
    profile_url = 'http://www.weibo.com/p/100505'+uid+'/info?mod=pedit'
    driver.get(profile_url)
    time.sleep(1)
    #step3: get profile information
    profile_url_2 = 'http://account.weibo.com/set/iframe?skin=skin048'
    driver.get(profile_url_2)
    time.sleep(1)
    profile_info_dict = {'uid': uid}
    #step4: get nickname
    uname_str = driver.find_element_by_xpath('//*[@id="pl_content_account"]/div[1]/div[1]/div[2]/div[2]')
    nick_name = uname_str.text
    profile_info_dict['screen_name'] = nick_name
    print 'nick_name:', nick_name
    #step5: get location
    location_str = driver.find_element_by_xpath('//*[@id="pl_content_account"]/div[1]/div[1]/div[4]/div[2]')
    location = location_str.text
    profile_info_dict['location'] = location
    print 'location:', location
    #step6: get gender
    gender_str = driver.find_element_by_xpath('//*[@id="pl_content_account"]/div[1]/div[1]/div[5]/div[2]')
    gender = gender_str.text
    profile_info_dict['gender'] = gender
    print 'gender:', gender
    #step7: get description
    description_str = driver.find_element_by_xpath('//*[@id="pl_content_account"]/div[1]/div[1]/div[12]/div[2]')
    description = description_str.text
    profile_info_dict['description'] = description
    print 'description:', description
    #step8: get birth
    birth_str = driver.find_element_by_xpath('//*[@id="pl_content_account"]/div[1]/div[1]/div[8]/div[2]')
    birth = birth_str.text
    profile_info_dict['birth'] = birth
    print 'birth:', birth
    #step9: get job
    try:
        job_str = driver.find_element_by_xpath('//*[@id="pl_content_account"]/div[3]/div[1]/div/div[2]/div/p[1]/a')
        job = job_str.text
    except:
        job = ''
    profile_info_dict['job'] = job
    print 'job:', job
    print 'profile_info_dict:', profile_info_dict
    
    driver.close()

if __name__=='__main__':
    uname = 'weiboxnr04@126.com'
    pwd = 'xnr123456'
    uid = '6346321407'
    get_userinfo(uname, pwd)
