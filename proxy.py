#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
import time
import json
import base64
import requests
import os
import hashlib
import string
import zipfile
import random


class Proxy(object):
    proxyServeAddr = "http://125.88.158.218:8082"
    proxyServePwd = "lovarkck"
    area = [] # 代理IP区域编号列表
    domain = ''
    port = 0
    user = ''
    passwd = ''
    

    def open(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6)'}
        url= "{}/open?api={}".format(self.proxyServeAddr, self.proxyServePwd)
        if len(self.area) > 0:
            url = self.proxyServeAddr + '/open?api={}&area={}'.format(self.proxyServePwd, self.area[random.randint(0, len(self.area)-1)])
        resp = requests.get(url, headers=headers)
        if resp:
            # print(resp.status_code, resp.json())
            if resp.status_code == 200:
                respJson = resp.json()
                if respJson['code'] == 200 and len(respJson['port']) > 0:
                    self.domain  = respJson['domain']
                    self.port = respJson['port'][0]
                    self.user = respJson['authuser']
                    self.passwd = respJson['authpass']
                    return respJson['domain'], respJson['port'][0], respJson['authuser'], respJson['authpass']

    def close(self, port=None):
        if port is None:
            port = self.port
        resp = requests.get(self.proxyServeAddr + '/close?api=pkajuzne&&port={}'.format(port))
        if resp and resp.status_code == 200:
            print("close proxy:", resp.json())


    def create_proxyauth_extension(self, scheme='http'):
        """代理认证插件
        args:
            proxy_host (str): 你的代理地址或者域名（str类型）
            proxy_port (int): 代理端口号（int类型）
            proxy_username (str):用户名（字符串）
            proxy_password (str): 密码 （字符串）
        kwargs:
            scheme (str): 代理方式 默认http
            plugin_path (str): 扩展的绝对路径

        return str -> plugin_path
        """

        self.plugin_path = '/tmp/chrome_proxyauth_plugin_{}_{}.zip'.format(self.domain, self.port)

        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = string.Template(
            """
        var config = {
                mode: "fixed_servers",
                rules: {
                singleProxy: {
                    scheme: "${scheme}",
                    host: "${host}",
                    port: parseInt(${port})
                },
                bypassList: ["foobar.com"]
                }
            };
    
        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
    
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "${username}",
                    password: "${password}"
                }
            };
        }
    
        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """
        ).substitute(
            host=self.domain,
            port=self.port,
            username=self.user,
            password=self.passwd,
            scheme=scheme
        )
        with zipfile.ZipFile(self.plugin_path, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)

        return self.plugin_path
