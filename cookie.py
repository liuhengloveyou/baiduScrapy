#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class Cookie(object):
    def __init__(self):
        pass

    def save(self):
        pass


###############################################################################
###############################################################################
if __name__ == "__main__":
    try:
        chromeProfilePath = '/Users/liuheng/dev/baiduScrapy/chromeProfile/userData';

        options = webdriver.ChromeOptions()
        options.add_argument("--user-data-dir={}".format(chromeProfilePath)); 
        driver = webdriver.Chrome(options = options)
        driver.get('https://baidu.com')

        time.sleep(200)        
    finally:
        driver.close()
        driver.quit()



