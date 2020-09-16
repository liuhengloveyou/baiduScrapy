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

def greenele(browser):
    i = 0
    windowstabs=browser.window_handles
    print(windowstabs)
    while len(windowstabs) == 1 and i <= 3:
        print("windowstabs: ", i, windowstabs)
        i = i+1
        time.sleep(1)
        windowstabs=browser.window_handles
    if len(windowstabs) == 1:
        return
    #切换到新窗口
    browser.switch_to.window(windowstabs[1])
   
    a_text=['首页', '摆地摊技巧', '摆地摊什么赚钱', '地摊交易', '地摊图片']
    for i in range(0, random.randint(3,7)):
        try:
            txt=a_text[random.randint(0,len(a_text)-1)]
            print(">>>>>>",txt)
            WebDriverWait(browser, 10).until(EC.visibility_of_all_elements_located((By.LINK_TEXT, txt)))
            WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, txt)))

            # 先滚动
            for j in range(0, random.randint(3,8)):
                browser.execute_script('window.scrollBy(0,{})'.format(800*random.random()))
                time.sleep(2*random.random())
            # 滚动顶
            time.sleep(2*random.random())
            for j in range(0, random.randint(1,6)):
                browser.execute_script('window.scrollBy(0,{})'.format(-800*random.random()))
                time.sleep(2*random.random())
            time.sleep(2*random.random())
            browser.execute_script("window.scrollTo(0,0);")

            # 点
            time.sleep(3*random.random())
            for btn in browser.find_elements_by_partial_link_text(txt):
                if btn.text == txt:
                    act = ActionChains(browser)
                    act.move_to_element(btn).perform()#定位鼠标到指定元素
                    act.click(btn).perform()
                    break
        except Exception as ex:
            s=sys.exc_info()  
            print("greenele ERR:", s[2].tb_lineno, ex)
            time.sleep(2)
            browser.refresh()
            browser.refresh()
    print(">>>end greenele")
    time.sleep(int(random.random()*2))
    browser.close()
    browser.switch_to.window(windowstabs[0])
    
###############################################################################
###############################################################################
if __name__ == "__main__":  
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True);
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument('lang=zh_CN.UTF-8')
        
    browser = webdriver.Chrome(options = options)
    browser.set_page_load_timeout(30)  # 设置页面加载超时
    browser.set_script_timeout(10)  # 设置页面异步js执行超时
    browser.implicitly_wait(10)
    browser.delete_all_cookies()
    try:
        browser.get('http://www.green-ele.com/')
        greenele(browser)
    finally:
        browser.close()



