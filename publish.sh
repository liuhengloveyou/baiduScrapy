#!/bin/bash

# https://chromedriver.storage.googleapis.com/78.0.3904.70/chromedriver_linux64.zip

# pip3 install cython
# pip3 install selenium
# pip3 install pytz

scp -i ~/dev/keys/southeast2.pem *.py  ubuntu@54.179.149.87:/opt/scrapy/

ssh -i ~/dev/keys/southeast2.pem ubuntu@54.179.149.87 "cd /opt/scrapy/; python3 setup.py build_ext --inplace; rm -rf *.c build;
rm -f baidu_com.py common.py setup.py ua.py main.py proxy.py;
rm babycarecn.*.so cn_9xzs.*.so main.*.so setup.*;
"

