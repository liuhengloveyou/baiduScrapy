#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
import time
import json
import base64
import requests
import os
import hashlib
import random
from datetime import datetime, timezone, timedelta
from pytz import timezone #pip3 install pytz

def mySleep():
    hour=datetime.fromtimestamp(int(time.time()), timezone('Asia/Shanghai')).hour

    s=0
    if hour == 0 or hour == 24:
        s=random.randint(60, 10*60) #1 ~ 10分钟
    elif hour >= 1 and hour < 5:
        s=random.randint(3*60, 10*60) # 3 ~ 10分钟
    elif hour == 5:
        s=random.randint(3*60, 5*60) # 3 ~ 5分钟
    elif hour == 6:
        s=random.randint(30, 120) # 0.5 ~ 2分钟
    elif hour == 7:
        s=random.randint(10, 30) # 10秒 ~ 30秒
    elif hour == 8:
        s=random.randint(2, 8) # 2秒 ~ 8秒
    elif hour >= 9 and hour <= 11:
        s=random.randint(0, 2) # 0 ~ 2秒
    elif hour == 12:
        s=random.randint(0,3) # 0 ~ 3秒
    elif hour == 13:
        s=random.randint(0,5) # 0 ~ 5秒
    elif hour >= 14 and hour <= 18:
        s=random.randint(0,2) # 0 ~ 2秒
    elif hour >= 19 and hour <= 21:
        s=random.randint(0,3) # 0 ~ 3秒
    elif hour > 21 and hour <= 23:
        s=random.randint(1,5) # 1 ~ 3秒
    print("本地时间为 :", hour, s)
    time.sleep(s)
    
def switchTab(browser, index):
    i = 0
    while i <= 3:
        windowstabs=browser.window_handles
        if len(windowstabs) >= index:
            # 切换到新窗口
            browser.switch_to.window(windowstabs[index])
            return True
        i = i+1
        time.sleep(1)
    return False

def sendHumanKeys(ele, text):
    for w in text:
        ele.send_keys(w)
        time.sleep(random.uniform(0.1, 1))
