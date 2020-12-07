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
sys.path.append("../")
from myscroll import Scroll

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



class keypleasure(object):
    browser=None
    a_text=['首页', "产品系列", "两性讲堂", "最新动向", "关于我们", "查验真伪"]


    def __init__(self, browser):
        self.browser = browser

    # 看产品1~2个
    def kancanpin(self):
        for i in range(0, random.randint(1, 2)):
            time.sleep(random.uniform(1, 2))
            try:                
                # 滚动下去
                for j in range(0, random.randint(3, 5)):
                    Scroll(self.browser).scrollDown()
                    time.sleep(random.uniform(0.5, 1.5))

                products = self.browser.find_elements_by_class_name("cpzi")
                ele = products[random.randint(0, len(products)-1)]
                ActionChains(self.browser).move_to_element(ele).perform()
                time.sleep(random.uniform(1, 2))
                ActionChains(self.browser).click(ele).perform()
                time.sleep(random.uniform(1, 2))

                # 滚动下去
                Scroll(self.browser).scrollToEnd()
                # 返回
                self.browser.back()
            except Exception as ex:
                print("kancanpin ERR:", sys.exc_info()[2].tb_lineno, ex)
    
    # 看讲堂1~2个
    def kanjiangtang(self):
        for i in range(0, random.randint(1, 2)):
            time.sleep(random.uniform(1, 2))
            try:
                # 滚动下去
                for j in range(0, random.randint(3, 5)):
                    Scroll(self.browser).scrollDown()
                    time.sleep(random.uniform(0.5, 1.5))

                products = self.browser.find_elements_by_class_name("wd11")
                ele = products[random.randint(0, len(products)-1)]
                ActionChains(self.browser).move_to_element(ele).perform()
                time.sleep(random.uniform(1, 2))
                ActionChains(self.browser).click(ele).perform()
                time.sleep(random.uniform(1, 2))

                # 滚动下去
                for j in range(0, random.randint(5,10)):
                    Scroll(self.browser).scrollDown()
                    time.sleep(random.uniform(0.5, 1))

                # 返回
                self.browser.back()
            except Exception as ex:
                print("kanjiangtang ERR:", sys.exc_info()[2].tb_lineno, ex)
    
    # 看动态0~1个
    def kandongtai(self):
        for i in range(0, random.randint(0, 1)):
            time.sleep(random.uniform(0.1, 2))
            try:
                # 滚动下去
                for j in range(0, random.randint(3, 6)):
                    Scroll(self.browser).scrollDown()
                    time.sleep(random.uniform(0.1, 1))

                products = self.browser.find_elements_by_class_name("xiaoxizi")
                ele = products[random.randint(0, len(products)-1)].find_element_by_tag_name("a")
                ActionChains(self.browser).move_to_element(ele).perform()
                time.sleep(3*random.random())
                ActionChains(self.browser).click(ele).perform()
                time.sleep(3*random.random())

                # 滚动下去
                for j in range(0, random.randint(5,10)):
                    Scroll(self.browser).scrollDown()
                    time.sleep(random.uniform(0.2, 1))

                # 返回
                self.browser.back()
            except Exception as ex:
                print("kandongtai ERR:", sys.exc_info()[2].tb_lineno, ex)


    def run(self):
        for i in range(0, random.randint(3, 6)):
            time.sleep(random.randint(1, 3))
            try:
                # 先滚动下去
                Scroll(self.browser).scrollToEnd()
                time.sleep(random.uniform(1, 3))
                # 再滚动到顶
                Scroll(self.browser).scrollToTop()
                
                txt=self.a_text[random.randint(0,len(self.a_text)-1)]
                print(txt)

                # 点
                WebDriverWait(self.browser, 30).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, txt)))
                for btn in self.browser.find_elements_by_partial_link_text(txt):
                    if btn.text == txt:
                        act = ActionChains(self.browser)
                        act.move_to_element(btn).perform()#定位鼠标到指定元素
                        act.click(btn).perform()
                        break

                if txt == "产品系列":
                    self.kancanpin()
                elif txt == "两性讲堂":
                    self.kanjiangtang()
                elif txt == "最新动向":
                    self.kandongtai()
                else:
                    # 滚动下去
                    Scroll(self.browser).scrollToEnd()
            
            except Exception as ex:
                print("keypleasure ERR:", sys.exc_info()[2].tb_lineno, ex)
                self.browser.refresh()
                self.browser.refresh()
                time.sleep(random.randint(1,2))
        time.sleep(random.randint(1,2))
        self.browser.close()
        self.browser.switch_to.window(self.browser.window_handles[0])
        return
    
###############################################################################
###############################################################################
if __name__ == "__main__":  
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument('lang=zh_CN.UTF-8')

    browser = webdriver.Chrome(options = options)
    browser.set_page_load_timeout(30)  # 设置页面加载超时
    browser.set_script_timeout(10)  # 设置页面异步js执行超时
    browser.implicitly_wait(10)
    browser.delete_all_cookies()
    try:
        browser.get('http://www.keypleasure.com.cn/')
        keypleasure(browser).run()
    finally:
        browser.close()


