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

import numpy as np # python3 -mpip install numpy --ignore-installed numpy
import scipy.interpolate as si

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

class Scroll(object):
    browser=None

    def __init__(self, browser):
        self.browser = browser

    # 向下滚动一次
    def scrollDown(self):
        tracks = [
            [(0, 0), (0, -6), (0, -17), (4, -76), (17, -143), (34, -222), (59, -305), (85, -388), (109, -452), (136, -525), (160, -582), (171, -609), (184, -640), (192, -660), (194, -666), (198, -675), (199, -677), (199, -678), (199, -678), (199, -678), (199, -677), (199, -677)],
            [(0, 0), (0, -9), (0, -28), (0, -47), (0, -64), (0, -76), (1, -83), (2, -91), (4, -96), (5, -98), (6, -105), (7, -108), (10, -116), (12, -122), (14, -125), (14, -127), (15, -128)],
            [(0, 0), (0, -10), (0, -19), (1, -49), (3, -80), (5, -103), (7, -132), (9, -156), (11, -166), (12, -176), (13, -180), (13, -185), (14, -189), (15, -193), (16, -196), (16, -197), (16, -198), (16, -199), (16, -199)],
            [(0, 0), (0, -9), (0, -19), (0, -50), (0, -113), (0, -165), (8, -219), (12, -248), (22, -303), (30, -338), (38, -367), (44, -388), (48, -397), (49, -405), (51, -408), (51, -409), (51, -410), (52, -410)],
            [(0, 0), (0, -11), (1, -17), (5, -44), (10, -75), (24, -134), (37, -174), (52, -222), (62, -254), (74, -290), (81, -314), (87, -332), (92, -345), (98, -359), (105, -372), (108, -380), (111, -386), (112, -389), (113, -390), (113, -391), (113, -390)],
            [(0, 0), (0, -1), (0, -1), (0, -2), (0, -3), (0, -7), (0, -12), (0, -19), (-1, -28), (-1, -29), (-2, -32), (-2, -33), (-2, -34), (-2, -34), (-2, -35), (-2, -36), (-2, -36), (-2, -37), (-2, -38), (-2, -38), (-3, -38), (-3, -38), (-3, -38)],
            [(0, 0), (0, -2), (0, -9), (0, -13), (2, -25), (5, -37), (8, -50), (12, -65), (13, -73), (14, -78), (14, -80), (15, -81), (15, -81)],
            [(0, 0), (0, 0), (0, -5), (0, -12), (0, -20), (-1, -31), (-3, -43), (-6, -57), (-10, -70), (-13, -79), (-16, -88), (-19, -100), (-20, -106), (-21, -113), (-22, -118), (-23, -121), (-23, -122), (-24, -122), (-24, -122)]
        ]
         
        points=tracks[random.randint(0,len(tracks)-1)]
        y = self.browser.execute_script("return document.documentElement.scrollTop || document.body.scrollTop;")
        for p in points:
            self.browser.execute_script('window.scrollTo({}, {})'.format(-1*p[0], y-p[1]))

    # 向上滚动一次
    def scrollUp(self):
        tracks = [
            [(0, 0), (0, 5), (0, 12), (0, 30), (-3, 80), (-5, 145), (-5, 204), (-5, 271), (-3, 356), (-2, 367), (5, 403), (12, 436), (20, 462), (26, 484), (30, 495), (34, 510), (35, 515), (36, 518), (36, 518)],
            [(0, 0), (0, 5), (0, 23), (-7, 84), (-14, 143), (-21, 205), (-25, 241), (-29, 278), (-31, 303), (-32, 323), (-32, 335), (-32, 343), (-32, 350), (-33, 353), (-33, 354)],
            [(0, 0), (0, 1), (0, 4), (0, 13), (0, 34), (0, 66), (0, 82), (0, 105), (0, 124), (0, 156), (0, 173), (0, 195), (0, 218), (0, 228), (0, 241), (1, 248), (1, 253), (1, 255), (1, 255)],
            [(0, 0), (0, 2), (0, 7), (0, 43), (0, 76), (-1, 111), (-1, 148), (-1, 173), (-1, 194), (-1, 213), (-1, 243), (-1, 265), (-2, 286), (-1, 301), (0, 312), (1, 327), (1, 333), (2, 339), (2, 344), (2, 348), (2, 350), (2, 352), (3, 353), (3, 355)],
            [(0, 0), (0, 4), (0, 19), (-6, 67), (-16, 121), (-20, 166), (-23, 201), (-23, 226), (-23, 244), (-23, 273), (-22, 300), (-18, 323), (-13, 348), (-10, 362), (-8, 376), (-7, 384), (-6, 389), (-6, 392), (-6, 394), (-6, 396), (-6, 396)],
            [(0, 0), (0, 0), (0, 2), (-1, 4), (-2, 10), (-6, 26), (-15, 55), (-43, 125), (-76, 212), (-107, 303), (-125, 363), (-149, 452), (-158, 502), (-163, 551), (-163, 601), (-163, 629), (-163, 646), (-162, 659), (-161, 664), (-160, 665), (-160, 666), (-160, 666), (-160, 668)]
        ]

        points=tracks[random.randint(0,len(tracks)-1)]

        y = self.browser.execute_script("return document.documentElement.scrollTop || document.body.scrollTop;")
        for p in points:
            self.browser.execute_script('window.scrollTo({}, {})'.format(-1*p[0], y-p[1]))

    # 滚动到底部
    def scrollToEnd(self):
        clientHeight = self.browser.execute_script("return document.documentElement.clientHeight || document.body.clientHeight;")
        scrollHeight = self.browser.execute_script("return document.documentElement.scrollHeight || document.body.scrollHeight;")
        scrollTop = self.browser.execute_script("return document.documentElement.scrollTop || document.body.scrollTop;")

        while (scrollTop + clientHeight) < (scrollHeight - 10):
            self.scrollDown()
            time.sleep(random.uniform(0.5, 2))
            scrollTop = self.browser.execute_script("return document.documentElement.scrollTop || document.body.scrollTop;")
    
    # 滚动到底部
    def scrollToTop(self):
        while self.browser.execute_script("return document.documentElement.scrollTop || document.body.scrollTop;") > 0:
            self.scrollUp()
            time.sleep(random.uniform(0.5, 1.5))
    

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
        browser.get('https://www.baidu.com/s?wd=selenium')
        time.sleep(3)
        Scroll(browser).scrollToEnd()
        time.sleep(3)
        Scroll(browser).scrollToTop()
    finally:
        browser.close()

