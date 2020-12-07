#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import time
import json
import base64
import requests
import os
import hashlib
import random
import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


def mfzwycom(browser):
        a_text=['网站首页', '摆地摊技巧', '摆地摊什么赚钱', '地摊交易', '地摊图片']

        for i in (0, 3):
            time.sleep(1)
            windowstabs=browser.window_handles
            if len(windowstabs) > 1:                
                browser.switch_to.window(windowstabs[1]) # 切换到新窗口
                break
        print(">>>>>>begin")

        for i in range(0, random.randint(3,5)):
            try:
                txt=a_text[random.randint(0,len(a_text)-1)]
                print("title>>>>>>",txt)
                WebDriverWait(browser, 2, 0.5).until(EC.element_to_be_clickable((By.LINK_TEXT, txt)))

                # 先滚动下去
                for j in range(0, random.randint(5,10)):
                    browser.execute_script('window.scrollBy(0,{})'.format(600*random.random()))
                    time.sleep(3*random.random())
                # 再滚上
                time.sleep(2*random.random())
                for j in range(0, random.randint(3,6)):
                    browser.execute_script('window.scrollBy(0,{})'.format(-800*random.random()))
                    time.sleep(2*random.random())

                # 点新闻
                news = browser.find_elements_by_class_name("news-item")
                if random.randint(1, 2) == 1 and len(news) > 1:
                    print("看新闻")
                    time.sleep(5*random.random())
                    ele = news[random.randint(0, len(news)-1)]
                    
                    ActionChains(browser).move_to_element(ele).perform()
                    ActionChains(browser).click(ele).perform()
                    # 滚动下去
                    time.sleep(3*random.random())
                    for j in range(0, random.randint(5, 10)):
                        browser.execute_script('window.scrollBy(0,{})'.format(500*random.random()))
                        time.sleep(2*random.random())
                    for j in range(0, random.randint(3,6)):
                        browser.execute_script('window.scrollBy(0,{})'.format(-800*random.random()))
                        time.sleep(2*random.random())

                browser.execute_script("window.scrollTo(0,0);")

                # 点导航
                WebDriverWait(browser, 5, 0.1).until(EC.element_to_be_clickable((By.LINK_TEXT, txt)))
                ele = browser.find_element_by_link_text(txt)
                ActionChains(browser).move_to_element(ele).click(ele).perform()
            except:
                browser.refresh()
                time.sleep(random.randint(1,2))
        print(">>>>>>end")
        time.sleep(int(random.random()*2))
        if len(browser.window_handles) > 1:                
            browser.close()
            browser.switch_to.window(windowstabs[0])
        
    
###############################################################################
###############################################################################
if __name__ == "__main__":
    browser = webdriver.Chrome()
    browser.set_page_load_timeout(30)  # 设置页面加载超时
    browser.set_script_timeout(10)  # 设置页面异步js执行超时
    browser.implicitly_wait(10)
    browser.delete_all_cookies()
    try:
        browser.get('http://www.mfzwy.com/')
        mfzwycom(browser)
    finally:
        browser.close()



