#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JiaChengXu'
__mtime__ = '2019/3/11'
"""

import threading
import random
import requests
from .Config import *
import time
import datetime
from .Logging import Logger
from bs4 import BeautifulSoup


class BaseSpider(object):
	TypesMap = {'二手房': 'ershoufang', '新房': 'loupan', '成交': 'chengjiao', '租房': 'zufang'}
	LimitPages = 10000000
	PerInPages = {k: v for k, v in zip(TypesMap.values(), [30, 10, 30, 30])}

	@classmethod
	def List2String(cls, List, symbol=','):
		String = ''
		for info in List:
			String += info + symbol
		return String[:-len(symbol)]

	def __init__(self, name=' ', filepath='./'):
		self.name = name
		self.re_conncet = 5
		today = datetime.datetime.now()
		self.date_string = today.strftime('%Y-%m-%d')
		self.date_path = filepath + today.strftime('%Y_%m_%d')
		self.num_of_records = 0
		self.title = None
		self.mutex = threading.Lock()  # 创建锁
		self.__start_logger()

	def grasp(self, url):
		headers = {'User-Agent': random.choice(UserAgents)}
		try:
			res = requests.get(url, headers=headers, timeout=TimeOut)
			html = res.text
		except:
			html = None
			self.logger.info('无法 得到 网页 %s 响应' % url)
		self.sleeping()
		return html

	def sleeping(self):
		if MaxSleep > 0:
			time.sleep((MaxSleep - MinSleep) * random.random() + MinSleep)

	def __start_logger(self):
		self.logger = Logger(self.date_path + '/', self.name).get_logger()
		self.logger.info('爬虫%s开始启动：' % self.name)

	def __get_info_in_per_url_ershoufang(self, soup):
		pass

	def __get_info_in_per_url_loupan(self, soup):
		pass

	def __get_info_in_per_url_zufang(self, soup):
		pass

	def __get_info_in_per_url_chengjiao(self, soup):
		pass

	def get_info_in_per_url(self, url, type_='chengjiao', fmt='csv'):
		data = self.grasp(url)
		if data is None:
			return []

		if type_ not in self.function_map.keys():
			self.logger.info('未知形式%s' % type_)
			return []

		soup = BeautifulSoup(data, 'lxml')
		func = self.function_map[type_]
		try:
			info_list = func(soup)
			if fmt == 'csv':
				inform = self.List2String(info_list)
				if isinstance(self.title, list):
					self.title = self.List2String(self.title)
			else:
				inform = info_list
		except Exception as error_info:
			inform = []
			self.logger.info('提取网页%s内容时发生错误' % url)
			self.logger.error(error_info)

		return inform

	def get_num_of_pages(self, url, types_):
		pass

	def get_urls_in_per_url(self, url, type_='chengjiao'):
		pass

	@property
	def function_map(self):
		return dict(loupan=self.__get_info_in_per_url_loupan, chengjiao=self.__get_info_in_per_url_chengjiao,
		            ershoufang=self.__get_info_in_per_url_ershoufang, zufang=self.__get_info_in_per_url_zufang)