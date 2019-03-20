#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JiaChengXu'
__mtime__ = '2019/3/14'
"""

from PyCrawler import BaseSpider
from bs4 import BeautifulSoup
from PyCrawler import LianJiaSpider
from PyCrawler import WoAiWoJiaSpider
import random
from PyCrawler.Config import UserAgents
from PyCrawler.Proxys import creat_proxys
import re
import requests
from selenium import webdriver
from PyCrawler.Driver import get_url

# url = 'https://su.lianjia.com/zufang/SU2208485643443773440.html'
# url = 'https://su.lianjia.com/zufang/SU2209438268959752192.html'
# url = 'https://su.lianjia.com/ershoufang/107101017801.html'
# url = 'https://su.lianjia.com/chengjiao/107100940226.html'
# url = 'https://su.fang.lianjia.com/loupan/p_zrgsscaftkn/xiangqing/'

# url = 'https://sz.5i5j.com/ershoufang/42426982.html'
# url = 'https://sz.5i5j.com/sold/38592474.html'

# url = 'https://sz.5i5j.com/ershoufang/42377740.html'
# url = 'https://sz.5i5j.com/ershoufang/41094586.html'
# url = 'https://sz.5i5j.com/sold/42377741.html'
# url = 'https://sz.5i5j.com/sold/42393301.html'
# url = 'https://sz.5i5j.com/sold/42156824.html'
# url = 'https://wap.5i5j.com/sz/loupan/xiangxi_19528.html'
# url = 'https://fang.5i5j.com/sz/loupan/xiangxi_19003.html'

# url = 'https://sz.5i5j.com/zufang/39696429.html'
# url = 'https://sz.5i5j.com/solds/'
# url = 'https://sz.5i5j.com/ershoufang/'
# url = 'https://sz.5i5j.com/zufang/'
url = 'https://fang.5i5j.com/sz/loupan/'

# url = 'https://su.lianjia.com/ershoufang/'
# url = 'https://su.lianjia.com/chengjiao/'
# url = 'https://su.lianjia.com/zufang/'
# url = 'https://su.fang.lianjia.com/loupan/'
# type_ = 'solds'
print(url)
#
#
# bs = BaseSpider.BaseSpider(name='test')
# html = bs.grasp(url)
# if html is not None:
#     soup = BeautifulSoup(html, 'lxml')


# tt = ['行政区', '楼盘', '均价', '开发商', '交房时间', '产权年限',  '绿化率', '容积率']

headers = {'User-Agent': random.choice(UserAgents),
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           }

wj = WoAiWoJiaSpider.WoAiWoJiaSpider(types='新房')
wj.run('url')
wj.run('information')
# urls = wj.get_urls_in_per_url(url, 'loupan')

