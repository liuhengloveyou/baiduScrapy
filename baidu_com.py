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

import pyautogui
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

from myscroll import Scroll
from common import *
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
        # options.add_argument('--headless') #浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
        options.page_load_strategy = 'eager' # DOM access is ready, but other resources like images may still be loading
        options.add_experimental_option('excludeSwitches', ['enable-automation']) # 关闭正受到自动测试软件的控制
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument('--disable-infobars') #防止Chrome显示“Chrome正在被自动化软件控制”的通知
        options.add_argument('––single-process')
        options.add_argument("--no-default-browser-check")
        options.add_argument('–-disable-plugins')
        options.add_argument("--disable-extensions")
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--ignore-certificate-errors")
        # options.add_argument('--no-sandbox') #解决DevToolsActivePort文件不存在的报错, 是让Chrome在root权限下跑
        # options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
        # options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
        # options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度
        # options.add_experimental_option("detach", True)

        # 设置chrome运行环境目录
        if self.userDataDir != None:
            options.add_argument("--user-data-dir={}".format(self.userDataDir))
        DiskCachePath = "{}/DiskCache".format(os.getcwd())
        if not os.path.exists(DiskCachePath):
            os.makedirs(DiskCachePath)
        options.add_argument("--disk-cache-dir={}".format(DiskCachePath))

        # 设置UA
        ua=UA().get()
        options.add_argument('user-agent=' + ua)

        # 设置代理
        if self.proxy != None:
            options.add_argument("--proxy-server=http://{}".format(self.proxy))
            # proxyauth_plugin_path = self.proxy.create_proxyauth_extension()
            # options.add_extension(proxyauth_plugin_path)    

        # self.browser = webdriver.Chrome(desired_capabilities=capabilities)
        self.browser = webdriver.Chrome(options = options)
        self.browser.set_window_size(1200+random.randint(0, 500), 800+random.randint(0, 500))
        self.browser.set_page_load_timeout(15)  # 设置页面加载超时
        self.browser.set_script_timeout(5)  # 设置页面异步js执行超时
        self.browser.implicitly_wait(1)

        # self.browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.browser.execute_script("Object.defineProperty(navigator, 'platform', {get: () => 'Win64'})")
        self.browser.execute_script('Object.defineProperty(navigator, "language", {get: () => ["zh-CN", "zh", "en"]});')
        self.browser.execute_script("Object.defineProperty(navigator, 'deviceMemory', {get: () => undefined});")
        self.browser.execute_script("Object.defineProperty(navigator, 'cpuClass', {get: () => undefined});")
        self.browser.execute_script("Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 8});")
        
        self.browser.execute_script('''
            var inject = function () {
            var overwrite = function (name) {
            const OLD = HTMLCanvasElement.prototype[name];
            Object.defineProperty(HTMLCanvasElement.prototype, name, {
                "value": function () {
                var shift = {
                    'r': Math.floor(Math.random() * 10) - 5,
                    'g': Math.floor(Math.random() * 10) - 5,
                    'b': Math.floor(Math.random() * 10) - 5,
                    'a': Math.floor(Math.random() * 10) - 5
                };
                var width = this.width, height = this.height, context = this.getContext("2d");
                var imageData = context.getImageData(0, 0, width, height);
                for (var i = 0; i < height; i++) {
                    for (var j = 0; j < width; j++) {
                    var n = ((i * (width * 4)) + (j * 4));
                    imageData.data[n + 0] = imageData.data[n + 0] + shift.r;
                    imageData.data[n + 1] = imageData.data[n + 1] + shift.g;
                    imageData.data[n + 2] = imageData.data[n + 2] + shift.b;
                    imageData.data[n + 3] = imageData.data[n + 3] + shift.a;
                    }
                }
                context.putImageData(imageData, 0, 0);
                return OLD.apply(this, arguments);
                }
            });
            };
            overwrite('toBlob');
            overwrite('toDataURL');
        };
        inject();''')
                
        # self.browser.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": ua})
        print("check UA: ", self.browser.execute_script("return navigator.userAgent;"))
        print("check webdriver: ", self.browser.execute_script("return window.navigator.webdriver;"))
        print("check platform: ", self.browser.execute_script("return window.navigator.platform;"))
        print("check plugins: ", self.browser.execute_script("return navigator.plugins.length;"))

    def clean(self):
        if self.browser != None:
            self.browser.quit()
    
    def onePage(self, currSearchKey):
        for i in range(0,2):
            time.sleep(random.uniform(0.5, 1))
            try:
                WebDriverWait(self.browser, 10).until(EC.title_contains(currSearchKey))
                WebDriverWait(self.browser, 10).until(EC.visibility_of_all_elements_located((By.XPATH, '//div[contains(@class, "result") and contains(@class, "c-container")]')))
                WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'n')))                
                WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.ID, 'su')))

                results=WebDriverWait(self.browser, 5, 0.2).until(lambda diver:self.browser.find_elements_by_xpath('//div[contains(@class, "result") and contains(@class, "c-container")]'))
                for result in results:
                    titleEle='' # 标题
                    urlEle='' # URL
                    gg='' # 广告标识

                    try:
                        titleEle=WebDriverWait(self.browser, 3, 0.2).until(lambda diver:result.find_element_by_xpath('h3/a'))
                        urlEle=result.find_element_by_class_name("c-showurl")
                        # ele=result.find_element_by_link_text("广告")
                        # gg=ele.text
                    except Exception as ex:
                        print("record ERR:", sys.exc_info()[2].tb_lineno, ex)
                        continue
                    # print("onePage: ", currSearchKey, urlEle.text, urlEle.text)
                    
                    # 广告跳过
                    if gg != '':
                        if random.randint(0, 100) == 0:
                            pass # 点广告
                        else:
                            continue # 广告跳过

                    # if (titleEle.text.find(self.task['title']) >= 0) and (urlEle.text.find(self.task['domain']) >= 0 or urlEle.text.find(self.task['title']) >= 0):
                    if urlEle.text.find(self.task['domain']) >= 0:
                        Scroll(self.browser).scrollDownIntoView(titleEle)
                        time.sleep(random.uniform(1, 2))
                        ActionChains(self.browser).click(titleEle).perform()
                        
                        if gg == '':
                            print("@@HIT: ", urlEle.text, "\ttitle: ", titleEle.text, "\t广告: ", gg)
                            return True # 不是广告才算点过，是广告继续
                return False
            except Exception as ex:
                print("record ERR:", ex, sys.exc_info()[2].tb_lineno)
                self.browser.refresh()
                time.sleep(random.uniform(1, 2))

    def oneKey(self, searchKeyWord):
        print('\n\nsearch word::', searchKeyWord)

        clicked = 0
        try:
            WebDriverWait(self.browser, 10, 0.2).until(EC.element_to_be_clickable((By.ID, 'su')))
            WebDriverWait(self.browser, 10, 0.2).until(EC.visibility_of_all_elements_located((By.ID, 'kw')))

            #@@@ 
            kw=self.browser.find_element_by_id("kw")
            su=self.browser.find_element_by_id("su")
            ActionChains(self.browser).move_to_element(kw).click(kw).perform()#定位鼠标到指定元素
            time.sleep(random.uniform(0.5, 2))
            sendHumanKeys(kw, searchKeyWord)
            
            ActionChains(self.browser).move_to_element(su).click(su).perform()
            WebDriverWait(self.browser, 10, 0.5).until(EC.title_contains(searchKeyWord))

            for p in range(1, random.randint(self.task['maxPage']-1, self.task['maxPage']+2)):
                WebDriverWait(self.browser, 10, 0.2).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, '下一页 >')))
                # WebDriverWait(self.browser, 10, 0.2).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="page"]/strong/span[2]'), '{}'.format(p)))
                #self.browser.find_element_by_xpath('//*[@id="page"]/strong/span[2]').text
                
                print('page: ', p)                
                finded = self.onePage(searchKeyWord)
                if clicked == 0 and True == finded:
                    time.sleep(random.uniform(0.5, 1.5))
                    clicked += 1
                    callback = self.task['callback']
                    switchTab(self.browser, 1)
                    callback(self.browser).run() # 具体网站的逻辑
                # 再往后看两页
                if clicked > 0:
                    clicked += 1
                if clicked > random.randint(1, 3):
                    time.sleep(random.random()*3)
                    break

                Scroll(self.browser).scrollToEnd()
                # 滚动至元素ele可见位置
                eles = self.browser.find_elements_by_css_selector('#rs table tr th a')
                if eles and len(eles) > 0:
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
                time.sleep(random.uniform(0.5, 2))
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



