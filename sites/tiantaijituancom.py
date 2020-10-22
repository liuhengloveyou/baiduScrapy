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

def tiantaijituan(browser):
    a_text=['首页', "产品中心", "公司概况", "招商合作", "关于我们", "会员注册", "第三终端招商", "新闻中心", "联系我们"]
    for i in range(0, random.randint(4,10)):
        try:
            txt=a_text[random.randint(0,len(a_text)-1)]
            print(">>>>>>",txt)
            WebDriverWait(browser, 10).until(EC.visibility_of_all_elements_located((By.LINK_TEXT, txt)))
            WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.LINK_TEXT, txt)))
            
            # 先滚动下去
            for j in range(0, random.randint(2,8)):
                browser.execute_script('window.scrollBy(0,{})'.format(800*random.random()))
                time.sleep(2*random.random())
            # 再滚动到顶
            time.sleep(2*random.random())
            for j in range(0, random.randint(1,6)):
                browser.execute_script('window.scrollBy(0,{})'.format(-800*random.random()))
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
            print("huimeisz ERR:", s[2].tb_lineno, ex)
            browser.refresh()
            time.sleep(1)
            browser.refresh()
            time.sleep(2)
    
###############################################################################
###############################################################################
if __name__ == "__main__":  
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True);
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
        
    browser = webdriver.Chrome(options = options)
    browser.set_page_load_timeout(30)  # 设置页面加载超时
    browser.set_script_timeout(10)  # 设置页面异步js执行超时
    browser.implicitly_wait(10)
    browser.delete_all_cookies()
    try:
        browser.get('http://www.tiantaijituan.com/')
        tiantaijituan(browser)
    finally:
        browser.close()



