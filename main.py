#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import time
import json
import base64
import os
import hashlib
import sys
import random

from proxy import Proxy
from baidu_com import baidu
from common import mySleep
from sites.tiantaijituancom import tiantaijituan
from sites.babycarecn import babycare

# http://www.tiantaijituan.com
huimeiszTask = {
    'keyWord': ['枸杞肽', '骨髓肽', '天肽生物', '枸杞肽'],
    'domain': 'www.tiantaijituan.com',
    'title': '善肽堂',
    'maxPage': 8,
    'callback': tiantaijituan
}

taskBabycare = {
    'keyWord': ['早教机构', '早教加盟', '幼儿早教'],
    'title': '东方爱婴',
    'domain': 'www.babycare.cn',
    'callback': babycare,
    'maxPage': 10,
}

###############################################################################
###############################################################################
if __name__ == "__main__":
    bai = None
    proxy = None
    random.seed()

    while True:
        print("#################################################################")
        print("#################################################################")
        mySleep()

        try:
            bai=baidu()
            bai.task = taskBabycare

            proxy = Proxy()
            # proxy.area = [110000, 440300, 440600, 445200, 440300, 440500, 440100, 310000, 441300]
            proxyDomain, proxyPort = proxy.open()
            print("proxy>>>", proxyDomain, proxyPort)
            
            outIP = proxy.getMyOutIP("http://{}:{}".format(proxyDomain, proxyPort))
            print("outIP>>>", outIP)

            # chromeProfile建目录
            if outIP != None:
                UserDataPath = "{}/UserData/{}".format(os.getcwd(), outIP["ip"].replace(".", "/"))
                if not os.path.exists(UserDataPath):
                    os.makedirs(UserDataPath)
                DiskCachePath = "{}/DiskCache/{}".format(os.getcwd(), outIP["ip"].replace(".", "/"))
                if not os.path.exists(DiskCachePath):
                    os.makedirs(DiskCachePath)
                bai.userDataDir = UserDataPath
                bai.diskCacheDir = DiskCachePath
            bai.proxy = "{}:{}".format(proxyDomain, proxyPort)
            
            bai.run()
        except Exception as ex:
            print("main ERR:", ex, sys.exc_info()[2].tb_lineno)
        finally:
            if proxy != None:
                proxy.close()
            if bai != None:
                bai.clean()    
        
    if proxy != None:
        proxy.close()
    if bai != None:
        bai.clean() 
