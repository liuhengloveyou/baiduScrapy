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

from baidu_com import baidu
from common import mySleep

def cn9xzs(browser):
    a_text=['家装案例', '公装案例', '北京装修', '选购主材', '联系我们', '回龙观装修', '环保家装', '装修知识']
    i = 0
    windowstabs=browser.window_handles
    print(windowstabs)
    while len(windowstabs) == 1 and i <= 3:
        print(windowstabs)
        i = i+1
        time.sleep(1)
        windowstabs=browser.window_handles
    if len(windowstabs) == 1:
            return
    #切换到新窗口
    browser.switch_to.window(windowstabs[1])

    if browser.current_url.find('m.9xzs.cn') >= 0:
        try:
            for i in range(0, random.randint(4,7)):
                txt=a_text[random.randint(0,len(a_text)-1)]
                print(">>>>>>cn9xzs",txt)
                WebDriverWait(browser, 10, 1).until(EC.element_to_be_clickable((By.LINK_TEXT, txt)))

                # 先滚动
                for j in range(0, random.randint(3,7)):
                    browser.execute_script('window.scrollBy(0,{})'.format(500*random.random()))
                    time.sleep(4*random.random())
                
                # 滚动到底
                browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")

                # 点
                time.sleep(3*random.random())
                for btn in browser.find_elements_by_xpath('//div[contains(@class, "footer-nav")]/a'):
                    if btn.text == txt:
                        act = ActionChains(browser)
                        act.move_to_element(btn).perform()#定位鼠标到指定元素
                        act.click(btn).perform()
                        # btn.click()
                        break

            time.sleep(random.randint(1,2))
        finally:
            browser.close()
            browser.switch_to.window(windowstabs[0])
    
###############################################################################
###############################################################################
if __name__ == "__main__":
    while True:
        mySleep()        
        try:
            b=baidu()
            b.area=110000
            b.searchKey=['回龙观装饰公司']
            b.siteName='久星装饰'
            b.siteDomain='m.9xzs.cn'
            b.openChrome()
            b.run(cn9xzs)
            # b.browser.get('http://m.9xzs.cn/')
            # cn9xzs(b.browser)
        finally:
            b.clean()



