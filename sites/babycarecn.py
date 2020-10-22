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

totalClickd=0 #点了多少次了

taskBabycare = {
    'keyWord': ['早教加盟', '早教机构'],
    'title': '东方爱婴',
    'domain': 'www.babycare.cn',
    'callback': babycare
}

def babycare(browser):
        a_text=['关于我们', '课程体系', '早教中心', '智能测评', '新闻中心', '中心查询', '我要加盟']
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
        # 切换到新窗口
        browser.switch_to.window(windowstabs[1])
        print(">>>>>>>>>>>>>>begin babycare")

        for i in range(0, random.randint(2,5)):
            try:
                txt=a_text[random.randint(0,len(a_text)-1)]
                print(">>>>>>>>>>>>>>babycare",txt)
                WebDriverWait(browser, 2, 0.1).until(EC.element_to_be_clickable((By.LINK_TEXT, txt)))
                # 先滚动
                for j in range(0, random.randint(4,7)):
                    browser.execute_script('window.scrollBy(0,{})'.format(600*random.random()))
                    time.sleep(3*random.random())

                WebDriverWait(browser, 3, 0.1).until(EC.element_to_be_clickable((By.LINK_TEXT, txt)))
                ele = browser.find_element_by_link_text(txt)
                ActionChains(browser).move_to_element(ele).click(ele).perform()
            except:
                browser.refresh()
                time.sleep(random.randint(1,2))
        print(">>>>>>end babycare")
        time.sleep(int(random.random()*2))
        browser.close()
        browser.switch_to.window(windowstabs[0])
    
###############################################################################
###############################################################################
if __name__ == "__main__":
    b=baidu()
    b.area=110000
    b.searchKey=['早教加盟', '早教机构'] #  '早教中心', '幼儿早教', '早教机构'
    b.siteName='东方爱婴'
    b.siteDomain='www.babycare.cn'
    b.callback = babycare
    b.openChrome()
    b.run()

    while True:
        mySleep()        
        try:
            b=baidu()
            b.area=110000
            b.searchKey=['早教加盟', '早教机构'] #  '早教中心', '幼儿早教', '早教机构'
            b.siteName='东方爱婴'
            b.siteDomain='www.babycare.cn'
            b.callback = babycare
            b.openChrome()
            b.run()
        finally:
            b.clean()
        totalClickd += 1
        print('totalClickd: ', totalClickd)



