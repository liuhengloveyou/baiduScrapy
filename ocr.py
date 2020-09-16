#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from aip import AipOcr


APP_ID = '18044940'
API_KEY = 'pTZxaKaexmxYFzf2RlpC9HQB'
SECRET_KEY = 'QtsjiC3ujEFZhtENydTpsROC3dfkLqpS'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

image = get_file_content('/Users/liuheng/Desktop/zhs_yzm1/1576485364.23.jpg')

options = {}
options["language_type"] = "CHN_ENG"
options["detect_direction"] = "false"
options["detect_language"] = "false"
options["probability"] = "true"

resp = client.basicGeneral(image, options);
print(resp)

# """ 如果有可选参数 """
# options = {}
# options["language_type"] = "CHN_ENG"
# options["detect_direction"] = "true"
# options["detect_language"] = "true"
# options["probability"] = "true"

# """ 带参数调用通用文字识别, 图片参数为本地图片 """
# client.basicGeneral(image, options)

# url = "https//www.x.com/sample.jpg"

# """ 调用通用文字识别, 图片参数为远程url图片 """
# client.basicGeneralUrl(url);

# """ 如果有可选参数 """
# options = {}
# options["language_type"] = "CHN_ENG"
# options["detect_direction"] = "true"
# options["detect_language"] = "true"
# options["probability"] = "true"

# """ 带参数调用通用文字识别, 图片参数为远程url图片 """
# client.basicGeneralUrl(url, options)