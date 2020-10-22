#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import time
import json
import base64
import os
import hashlib
import sys

from proxy import Proxy
from baidu_com import baidu
from common import mySleep
from sites.tiantaijituancom import tiantaijituan


# http://www.tiantaijituan.com
huimeiszTask = {
    'keyWord': ['骨髓肽', '枸杞肽', '天肽生物'],
    'domain': 'www.tiantaijituan.com',
    'title': '善肽堂',
    'maxPage': 5,
    'callback': tiantaijituan
}

###############################################################################
###############################################################################
if __name__ == "__main__":
    bai = None
    proxy = None

    while True:
        mySleep()

        try:
            bai=baidu()
            bai.task = huimeiszTask

            proxy = Proxy()
            proxy.area = [110000, 440300, 440600, 445200, 440300, 440500, 440100, 310000, 441300]
            proxyDomain, proxyPort = proxy.open()
            print("proxy>>>", proxyDomain, proxyPort)
            
            outIP = proxy.getMyOutIP("http://{}:{}".format(proxyDomain, proxyPort))
            print("outIP>>>", outIP)

            # chromeProfile建目录
            if outIP != None:
                path = "{}/chromeProfile/{}".format(os.getcwd(), outIP["ip"].replace(".", "/"))
                if not os.path.exists(path):
                    os.makedirs(path)
                bai.chromeProfilePath = path
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
