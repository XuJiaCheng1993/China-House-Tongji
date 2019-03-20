#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JiaChengXu'
__mtime__ = '2019/3/17'
"""
import requests
import random
from .Config import *
from bs4 import BeautifulSoup

def creat_proxys():
	headers = {'User-Agent': random.choice(UserAgents)}

	try:
		url = 'http://www.xicidaili.com/nt/1'
		req = requests.get(url, headers=headers)
		source_code = req.content
		soup = BeautifulSoup(source_code, 'lxml')
		ips = soup.findAll('tr')
		proxys_src = []
		for x in range(1, len(ips)):
			ip = ips[x]
			tds = ip.findAll("td")
			proxy_host = "{0}://".format(tds[5].contents[0]) + tds[1].contents[0] + ":" + tds[2].contents[0]
			proxy_temp = {tds[5].contents[0]: proxy_host}
			proxys_src.append(proxy_temp)
			if x >= ProxysNum:
				break
	except Exception as error_info:
		proxys_src = {}
		print("spider_proxyip exception:")
		print(error_info)

	return proxys_src

