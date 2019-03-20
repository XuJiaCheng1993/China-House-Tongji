#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JiaChengXu'
__mtime__ = '2019/3/18'
"""

import json
from PyCrawler.LianJiaSpider import LianjiaSpider
from PyCrawler.WoAiWoJiaSpider import WoAiWoJiaSpider

with open('./MyConfig.txt', 'r') as file_obj:
	myconfigs = json.load(file_obj)

types_alias = ['CJ', 'ESF', 'ZF', 'XF']
types_ = ['成交', '二手房', '租房', '新房']

file_path = myconfigs['DataSavePath']


lj_params = myconfigs['SuzhouLiaJia']
for i in range(4):
	lj_spider = LianjiaSpider(file_path=file_path, city='苏州', types=types_[i])
	for args in lj_params[types_alias[i]]:
		lj_spider.run('url', *args)
	lj_spider.run('information')
	del lj_spider

wj_params = myconfigs['Suzhou5i5j']
for i in range(4):
	wj_spider = WoAiWoJiaSpider(file_path=file_path, city='苏州', types=types_[i])
	for args in wj_params[types_alias[i]]:
		wj_spider.run('url', *args)
	wj_spider.run('information')
	del wj_spider