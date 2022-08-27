#!/usr/bin/env bash

pip3 install virtualenv

virtualenv venv

source ~/.venv/bin/activate

#退出当前的venv环境
# deactivate 

pip3 install selenium
pip3 install requests
pip3 install pytz
python3 -mpip install numpy --ignore-installed numpy
python3 -mpip install numpy scipy matplotlib
pip3 install python-dateutil
