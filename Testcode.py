#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JiaChengXu'
__mtime__ = '2019/3/14'
"""

from PyHouse.crawler import BaseSpider, LianJiaSpider, WoAiWoJiaSpider, FiveKHouseSpider

from bs4 import BeautifulSoup

import random
from PyCrawler.Config import UserAgents
from PyCrawler.Proxys import creat_proxys
import re
import requests
from selenium import webdriver
from PyCrawler.Driver import get_url
from requests.utils import dict_from_cookiejar, cookiejar_from_dict
import urllib3



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

# url = 'http://cs.5khouse.com/sell/selldetail1639137.aspx'
# url = 'http://cs.5khouse.com/sell/selllist.aspx'
# url = 'http://cs.5khouse.com/community/communitylist.aspx'
# url = 'http://cs.5khouse.com/community/communityselllist_-r38.aspx'

url = 'http://cs.5khouse.com/community/communityselllist_-r479-b-c-p12.aspx'

# url = 'https://sz.5i5j.com/zufang/39696429.html'
# url = 'https://sz.5i5j.com/solds/'
# url = 'https://sz.5i5j.com/ershoufang/'
# url = 'https://sz.5i5j.com/zufang/'
# url = 'https://fang.5i5j.com/sz/loupan/'

# url = 'https://su.lianjia.com/ershoufang/'
# url = 'https://su.lianjia.com/chengjiao/'
# url = 'https://su.lianjia.com/zufang/'
# url = 'https://su.fang.lianjia.com/loupan/'
# type_ = 'solds'
print(url)
#
# #
bs = BaseSpider.BaseSpider(name='test')
html = bs.grasp(url)
if html is not None:
    soup = BeautifulSoup(html, 'lxml')

# fk = FiveKHouseSpider.FivekSpider(types='小区')
# num = fk.get_num_of_pages(url, 'ershoufang')
# pg = fk._get_url_list_for_run(area='0-0', conditions='-b-c-d-f-g-h-i-j-k5-l')
# fk.run('url')

# urls = fk._get_url_list_for_run_community()

fk = FiveKHouseSpider.FivekSpider(types='二手房')
# fk.run('url')
fk.run('information')

# pg = fk._get_url_list_for_run()
# pg = fk.get_urls_in_per_url(url, type_='sell')


# detail_1 =  soup.select('.house dt a' )
# urls = list(set([f['href'] for f in detail_1]))
#
# sellurls = [f for f in urls if f.find('communityselllist') >= 0]
# renturls = [f for f in urls if f.find('communityrentlist') >= 0]

# fk.run('url', area='4-0', conditions='-b-c-d-f-g-h-i-j5-k-l')
# fk.run('information')

# urls = fk.get_urls_in_per_url(url, 'ershoufang')
# # info = fk.get_info_in_per_url_ershoufang(soup)
#
# info = fk.get_info_in_per_url(urls[0], 'ershoufang')


# tj = soup.select('.tj')[0].text.split('/')[-1]

# url_info = soup.select('.house li a')
# page_url = [pg_url['href'] for pg_url in url_info]
# urls = [f for f in list(set(page_url)) if f.find('selldetail') >= 0]













# SessionId = BaseSpider.generate_session_id()
# # tt = ['行政区', '楼盘', '均价', '开发商', '交房时间', '产权年限',  '绿化率', '容积率']
# print(SessionId)
#
# headers = {'User-Agent': random.choice(UserAgents),
#            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#            }

# wj = WoAiWoJiaSpider.WoAiWoJiaSpider(types='新房')
# wj.run('url')
# wj.run('information')
# urls = wj.get_urls_in_per_url(url, 'loupan')

# html = requests.get(url, headers = headers,)

# html = requests.get(url, headers = headers, cookies= cookiejar_from_dict({'PHPSESSID':SessionId}))
# cookies = dict_from_cookiejar(html.cookies)
# print(cookies)

# url = 'https://passport.5i5j.com/passport/login?service=https%3A%2F%2Fsz.5i5j.com%2Freglogin%2Findex%3FpreUrl%3Dhttps%253A%252F%252Fsz.5i5j.com%252F%status=1&city=sz'
# url1 = 'https://passport.5i5j.com/passport/login?service=https%3A%2F%2Fbj.5i5j.com%2Freglogin%2Findex%3FpreUrl%3Dhttps%253A%252F%252Fbj.5i5j.com%252F&status=1&city=bj'
# url2 = 'https://bj.5i5j.com/user/index/'
# #
# html = requests.post(url2, data={'username':'18260160581', 'password':'WIWJ123456'},  headers = headers,)
# cookies = dict_from_cookiejar(html.cookies)
# #
# print(cookies)