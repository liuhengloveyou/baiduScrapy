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
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from baidu_com import baidu

def login(browser):
    # browser.get('https://ziyuan.baidu.com/login/index')
    print(">>>login")
    browser.get("http://www.baidu.com")
    #进入百度首页，点击登陆，进入登陆页面
    login = browser.find_element_by_id("u1").find_element_by_class_name("lb")
    login.click()
    time.sleep(2)
    #进入登陆页面后，选择用户密码登陆
    usrLogin =browser.find_element_by_id("TANGRAM__PSP_10__footerULoginBtn")
    usrLogin.click()
    #输入用户名
    browser.find_element_by_id("TANGRAM__PSP_10__userName").send_keys("17688396387")
    time.sleep(1)
    #输入密码
    browser.find_element_by_id("TANGRAM__PSP_10__password").send_keys("wzseo~BD$$1688")
    time.sleep(1)
    browser.find_element_by_id("TANGRAM__PSP_10__submit").click()

def captcha(browser):
    browser.get('https://ziyuan.baidu.com/')

    time.sleep(100)
    



###############################################################################
###############################################################################
if __name__ == "__main__":
    try:
        b=baidu()
        b.openChrome()
        login(b.browser)
        captcha(b.browser)
    finally:
        b.clean()


