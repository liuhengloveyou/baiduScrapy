#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import time
import json
import base64
#import requests
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
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from common import mySleep
from proxy import Proxy
from ua import UA

class baidu(object):
    browser=None
    userDataDir=None
    proxy=None # 127.0.0.1:8080
    task=None

    def __init__(self):
        pass

    def openChrome(self):
        options = webdriver.ChromeOptions()
        options.page_load_strategy = 'eager' # DOM access is ready, but other resources like images may still be loading
        # options.add_experimental_option("detach", True)
        options.add_experimental_option('excludeSwitches', ['enable-automation']) # 关闭正受到自动测试软件的控制
        options.add_argument('--headless') #浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
        options.add_argument('--disable-infobars') #防止Chrome显示“Chrome正在被自动化软件控制”的通知
        options.add_argument('––single-process')
        options.add_argument("--no-default-browser-check")
        options.add_argument('–-disable-plugins')
        options.add_argument("--disable-extensions")
        options.add_argument('--no-sandbox') #解决DevToolsActivePort文件不存在的报错, 是让Chrome在root权限下跑
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--ignore-certificate-errors")
        # options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度
        # options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
        # options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
        

        # 设置chrome运行环境目录
        if self.userDataDir != None:
            options.add_argument("--user-data-dir={}".format(self.userDataDir))
        # if self.diskCacheDir != None:
        #     options.add_argument("--disk-cache-dir={}".format(self.diskCacheDir))

        # 设置UA
        ua=UA().get()
        options.add_argument('user-agent=' + ua)
        print('ua>>>: ', ua)

        # 设置代理
        if self.proxy != None:
            options.add_argument("--proxy-server=http://{}".format(self.proxy))
            # proxyauth_plugin_path = self.proxy.create_proxyauth_extension()
            # options.add_extension(proxyauth_plugin_path)    

        # self.browser = webdriver.Chrome(desired_capabilities=capabilities)
        self.browser = webdriver.Chrome(options = options)
        self.browser.set_window_size(1200+random.randint(0, 500), 1000+random.randint(0, 500))
        self.browser.set_page_load_timeout(30)  # 设置页面加载超时
        self.browser.set_script_timeout(10)  # 设置页面异步js执行超时
        self.browser.implicitly_wait(10)

    def clean(self):
        if self.browser != None:
            self.browser.quit()
    
    def onePage(self, currSearchKey):
        for i in range(0,2):
            time.sleep(random.random()*2)
            try:
                WebDriverWait(self.browser, 10).until(EC.title_contains(currSearchKey))
                WebDriverWait(self.browser, 10).until(EC.visibility_of_all_elements_located((By.XPATH, '//div[contains(@class, "result") and contains(@class, "c-container")]')))
                WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'n')))                
                WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.ID, 'su')))
                
                results=self.browser.find_elements_by_xpath('//div[contains(@class, "result") and contains(@class, "c-container")]')
                for result in results:
                    titleEle=''
                    urlEle=''
                    gg=''
                    try:
                        titleEle=result.find_element_by_xpath('h3/a')
                        urlEle=result.find_element_by_class_name("c-showurl")
                        # ele=result.find_element_by_link_text("广告")
                        # gg=ele.text
                    except Exception as ex:
                        print("one record ERR:", sys.exc_info()[2].tb_lineno, ex)
                        continue
                    # print(">>>url: ", urlEle.text, "\ttitle: ", titleEle.text, "\t广告: ", gg)
                    
                    # 广告跳过
                    if gg != '':
                        if random.randint(0, 100) == 0:
                            pass # 点广告
                        else:
                            continue # 广告跳过

                    if (titleEle.text.find(self.task['title']) >= 0) and (urlEle.text.find(self.task['domain']) >= 0 or urlEle.text.find(self.task['title']) >= 0):
                        time.sleep(random.random()*2)
                        self.browser.execute_script('window.scrollBy(0,{})'.format(int(300*random.random())))
                        self.browser.execute_script("arguments[0].scrollIntoView();", titleEle)
                        self.browser.execute_script("arguments[0].focus();", titleEle) # 显示到这条结果
                        
                        time.sleep(random.random()*2)
                        self.browser.execute_script('window.scrollBy(0,{})'.format(-1*random.randint(150,260)))
                        time.sleep(random.random()*3)
                        titleEle.click()
                        if gg == '':
                            print("@@@@@@: ", urlEle.text, "\ttitle: ", titleEle.text, "\t广告: ", gg)
                            return True # 不是广告才算点过，是广告继续
                return False
            except Exception as ex:
                print("record ERR:", ex, sys.exc_info()[2].tb_lineno)
                self.browser.refresh()
                time.sleep(1)
                self.browser.refresh()
                time.sleep(random.randint(1,2))

    def oneKey(self, searchKeyWord):
        clicked = 0

        try:
            self.browser.execute_script('window.scrollTo(0,0)')
            WebDriverWait(self.browser, 10, 0.2).until(EC.element_to_be_clickable((By.ID, 'su')))
            WebDriverWait(self.browser, 10, 0.2).until(EC.visibility_of_all_elements_located((By.ID, 'kw')))

            kw=self.browser.find_element_by_id("kw")
            ActionChains(self.browser).move_to_element(kw).click(kw).perform()#定位鼠标到指定元素
            time.sleep(random.random()/2)
            kw.clear()
            kw.send_keys(searchKeyWord)
            su=self.browser.find_element_by_id("su")
            ActionChains(self.browser).move_to_element(su).click(su).perform()
            WebDriverWait(self.browser, 10, 0.5).until(EC.title_contains(searchKeyWord))

            for p in range(1, random.randint(self.task['maxPage']-1, self.task['maxPage']+3)):
                WebDriverWait(self.browser, 10, 0.2).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, '下一页 >')))
                # WebDriverWait(self.browser, 10, 0.2).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="page"]/strong/span[2]'), '{}'.format(p)))
                #self.browser.find_element_by_xpath('//*[@id="page"]/strong/span[2]').text
                
                print('page>>>', p, searchKeyWord)                
                finded = self.onePage(searchKeyWord)
                if clicked == 0 and True == finded:
                    time.sleep(random.random())
                    clicked += 1
                    callback = self.task['callback']
                    if callback != None:
                        callback(self.browser) # 具体网站的逻辑
                # 再往后看两页
                if clicked > 0:
                    clicked += 1
                if clicked > random.randint(1, 3):
                    time.sleep(random.random()*3)
                    break

                # 下一页
                for k in range(0, random.randint(3, 6)):
                    self.browser.execute_script('window.scrollBy(0,{})'.format(600*random.random()))
                    time.sleep(random.random()*1.5)
                # 滚动至元素ele可见位置
                eles = self.browser.find_elements_by_css_selector('#rs table tr th a')
                if eles and len(eles) > 0:
                    time.sleep(random.random()*3)
                    ele = eles[0]
                    self.browser.execute_script("arguments[0].scrollIntoView();",ele)
                    nextPage = self.browser.find_element_by_partial_link_text("下一页 >")
                    ActionChains(self.browser).move_to_element(nextPage).perform()#定位鼠标到指定元素
                    ActionChains(self.browser).click(nextPage).perform()
                    time.sleep(random.random())
        except Exception as ex:
            s=sys.exc_info()  
            print("oneKey ERR:", ex, s[2].tb_lineno)
        
    
    def run(self):
        if self.task == None:
            print("task None")
            return
        cb = self.task["callback"]
        if cb == None:
            print("task.callback None")
            return

        self.openChrome()
        try:
            self.browser.get("https://www.baidu.com/")
            for key in range(0, random.randint(1, len(self.task['keyWord']))):
                currSearchKey = self.task['keyWord'][random.randint(0, len(self.task['keyWord'])-1)]
                time.sleep(random.randint(1, 3))
                print('\n\nsearch oneKey>>>', currSearchKey)                
                self.oneKey(currSearchKey)                
        except Exception as ex:
            s=sys.exc_info()  
            print("ERR: ", ex, s[2].tb_lineno)

###############################################################################
###############################################################################
if __name__ == "__main__":
    try:
        b=baidu()
        b.openChrome()
        b.run()
    finally:
        b.clean()



