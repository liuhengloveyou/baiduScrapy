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
from sites.babycarecn import babycare
from sites.greenele import greenele
from sites.huimeisz import huimeisz

taskBabycare = {
    'keyWord': ['早教加盟', '早教机构'],
    'title': '东方爱婴',
    'domain': 'www.babycare.cn',
    'callback': babycare
}
greeneleTask = {
    'keyWord': ['摆地摊'],
    'domain': 'green-ele',
    'title': '绿色地摊创业项目网',
    'maxPage': 5,
    'callback': greenele
}

# https://www.huimeisz.com/
huimeiszTask = {
    'keyWord': ['theraderm'],
    'domain': 'huimeisz.com',
    'title': 'Theraderm丝莱得代理',
    'maxPage': 5,
    'callback': huimeisz
}

###############################################################################
###############################################################################
if __name__ == "__main__":
    while True:
        mySleep()

        proxy = None
        b= None
        try:
            proxy = Proxy()
            proxy.area = [440300, 440600, 445200, 440300, 440500, 440100, 310000]

            b=baidu()
            b.proxy = proxy
            b.task = greeneleTask
            b.run()
        except Exception as ex:
            s=sys.exc_info()  
            print("main ERR:", ex, s[2].tb_lineno)
        finally:
            proxy.close()
            b.clean()
            