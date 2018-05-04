# coding=utf-8

import sys 
reload(sys)
sys.setdefaultencoding('utf-8') 
import json
import time            
import re            
import os
import codecs  
import shutil
import urllib 
import random
from urllib import quote
from selenium import webdriver        
from selenium.webdriver.common.keys import Keys        
import selenium.webdriver.support.ui as ui        
from selenium.webdriver.common.action_chains import ActionChains
from BeautifulSoup import BeautifulSoup
import random
from pyvirtualdisplay import Display
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

display = Display(visible=0, size=(1024,768))
display.start()

try:
    # 安管中心环境使用####
    driver = webdriver.Firefox()
except:
    # 213环境使用########
    cap = DesiredCapabilities().FIREFOX
    cap["marionette"] = False
    driver = webdriver.Firefox(capabilities=cap)

source_list = [
"http://widget.weibo.com/dialog/PublishWeb.php?refer=y&app_src=3o33sO&button=pubilish", # 发布窗
"http://widget.weibo.com/dialog/PublishWeb.php?refer=y&app_src=5yrCy2&button=pubilish", # 爱尖刀科技媒体
"http://widget.weibo.com/dialog/PublishWeb.php?refer=y&app_src=19mGfK&button=%E4%BD%9C%E8%19mGfK80%85@laenix", # Nexus6
]

def login_m_weibo_cn(username, password):
    print u'准备登陆Weibo.cn网站...'
    driver.get("https://passport.weibo.cn/signin/login?entry=mweibo&r=http%3A%2F%2Fm.weibo.cn")
    # sleep 以应对没出现相应元素
    time.sleep(5)
    driver.find_element_by_id("loginName").clear()
    driver.find_element_by_id("loginName").send_keys(username) #用户名
    driver.find_element_by_id("loginPassword").clear()
    driver.find_element_by_id("loginPassword").send_keys(password)  #密码
    driver.find_element_by_id("loginAction").send_keys(Keys.RETURN)
    # sleep以应对验证码
    time.sleep(10)

def publish_by_source(text):
    #url = random.choice(source_list)
    url = source_list[2]
    driver.get(url)
    try:
        texta = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[1]/div/div[2]/textarea")
    except:
        texta = driver.find_element_by_xpath("/html/body/section[1]/section/section[1]/div/div[2]/textarea")
    texta.send_keys(text)
    time.sleep(5)
    try:
        driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[2]/a").click()
    except:
        driver.find_element_by_xpath("//*[@id=\"pl_publish_publishMobile\"]/section/section[1]/div/div[3]/div/a[3]").click()

def publish_by_source_with_picture(text, file):
    #url = random.choice(source_list)
    url = source_list[2]
    driver.get(url)
    try:
        texta = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[1]/div/div[2]/textarea")
    except:
        texta = driver.find_element_by_xpath("/html/body/section[1]/section/section[1]/div/div[2]/textarea")
    texta.send_keys(text)
    time.sleep(1)
    driver.find_element_by_xpath('//a[@title="图片"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//input[@id="activity_img"]').send_keys(file)
    time.sleep(1)
    try:
        driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[2]/a").click()
    except:
        driver.find_element_by_xpath("//*[@id=\"pl_publish_publishMobile\"]/section/section[1]/div/div[3]/div/a[3]").click()


def weibo_publish(username,password,text):
    login_m_weibo_cn(username, password)
    publish_by_source(text)
    driver.quit()
    display.stop()

def weibo_publish_with_picture(username,password,text,file):
    login_m_weibo_cn(username, password)
    publish_by_source_with_picture(text, file)
    driver.quit()
    display.stop()


def weibo_publish_main(username,password,text,file):
    
    try:
    
        if file:
            weibo_publish_with_picture(username,password,text,file)
        else:
            weibo_publish(username,password,text)

        mark = True

    except:

        mark = False

    return mark


if __name__ == '__main__':
    #定义变量
    username = 'weiboxnr04@126.com' #输入你的用户名
    password = 'xnr1234567' #输入你的密码
    text = '测试oook'.decode('utf-8')
    file = '/home/ubuntu8/yuanhuiru/xnr/xnr1/xnr/sina/640.jpg'

    if file:
        weibo_publish_with_picture(username,password,text,file)
    else:
        weibo_publish(username,password,text)
