#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JiaChengXu'
__mtime__ = '2019/3/11'
"""
import threadpool
import os
import threading
import random
import requests
import time
import datetime
from .Logging import Logger
from bs4 import BeautifulSoup
from .Config import *
from .Proxys import creat_proxys
from tqdm import tqdm
from requests.utils import cookiejar_from_dict


def generate_session_id():
	string = 'abcdefghijklmnopqrstuvwxyz0123456789'
	id = ''
	for i in range(26):
		id += random.choice(string)
	return id


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

	def __init__(self, name=' ', filepath='./', re_connect=5):
		self.name = name
		self.re_connect = re_connect
		today = datetime.datetime.now()
		self.date_string = today.strftime('%Y-%m-%d')
		self.date_path = filepath + today.strftime('%Y_%m_%d')
		self.num_of_records = 0
		self.err_times = 0
		self.title = None
		self.mutex = threading.Lock()  # 创建锁
		self.__start_logger()

	def grasp(self, url):
		try:
			html = None
			for i in range(self.re_connect):
				headers = {'User-Agent': random.choice(UserAgents),
				           }
				proxies = creat_proxys() if Proxys else {}
				if proxies:
					proxies = random.choice(proxies)

				self.sleeping()
				result = requests.get(url, headers=headers, proxies=proxies, timeout=TimeOut,
				                      )
				status = result.status_code
				if status == 200:
					html = result.text
					break
				self.logger.info('无法 得到 网页 %s 响应 Status %s' % (url, status))
				self.logger.info(result.text)

		except:
			html = None
			self.logger.info('无法 得到 网页 %s 响应' % url)
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

	def get_urls_in_per_url(self, url, type_):
		pass

	def get_info_in_per_url(self, url, type_, fmt='csv'):
		data = self.grasp(url)
		if data is None:
			return []

		if type_ not in self.function_map.keys():
			self.logger.info('收集网页信息时，未知形式%s' % type_)
			return []

		soup = BeautifulSoup(data, 'lxml')
		func = self.function_map[type_]
		try:
			info_list = func(soup)
			if fmt == 'csv':
				inform = self.List2String(info_list)
			else:
				inform = info_list
		except Exception as error_info:
			inform = []
			self.logger.info('提取网页%s内容时发生错误, 使用函数%s' % (url, func))
			self.logger.exception(error_info)
		return inform

	def __collect_and_save_urls(self, url):
		urls = self.get_urls_in_per_url(url, self.type_)

		if urls:
			self.mutex.acquire()
			for u in urls:
				if u:
					self.url_file.write(u + '\n')
			self.num_of_url_records += 1
			self.pbar.update(1)
			self.mutex.release()

	def __run_for_urls(self, url_file, page_url_list):
		self.pbar = tqdm(total=len(page_url_list), desc='Collect URLs')
		self.num_of_url_records = 0
		with open(url_file, 'a+', encoding='utf-8-sig') as self.url_file:
			arg = zip(zip(page_url_list), [None, ] * len(page_url_list))
			pool = threadpool.ThreadPool(MaxThread)
			my_requests = threadpool.makeRequests(self.__collect_and_save_urls, arg)
			[pool.putRequest(req) for req in my_requests]
			pool.wait()
			pool.dismissWorkers(MaxThread, do_join=True)  # 完成后退出
		self.pbar.close()

	def __collect_and_save_info_in_per_url(self, url):

		info = self.get_info_in_per_url(url, self.type_)

		self.mutex.acquire()
		if info:
			self.info_file.write(self.date_string + "," + info + "\n")
			self.num_of_records += 1
			self.pbar.update(1)
		else:
			self.err_times += 1
		self.mutex.release()



	def __run_for_information(self, url_file, info_file):
		with open(url_file, 'rb') as file:
			lines = file.readlines()
		urls = [line.decode().split('\ufeff')[-1].split('\r')[0] for line in lines]
		urls = list(set(urls))

		self.pbar = tqdm(total=len(urls), desc='Collect Data')
		with open(info_file, 'w+', encoding='utf-8-sig') as self.info_file:
			if self.title is not None:
				if isinstance(self.title, list):
					title = self.List2String(self.title)
					self.info_file.write("采集时间," + title + "\n")
			arg = zip(zip(urls), [None, ] * len(urls))
			pool = threadpool.ThreadPool(MaxThread)
			my_requests = threadpool.makeRequests(self.__collect_and_save_info_in_per_url, arg)
			[pool.putRequest(req) for req in my_requests]
			pool.wait()
			pool.dismissWorkers(MaxThread, do_join=True)  # 完成后退出
		self.pbar.close()


	def _get_save_file_name(self):
		pass

	def _get_url_list_for_run(self, area, conditions):
		pass

	def run(self, mode, area=None, conditions=None):
		url_file, info_file = self._get_save_file_name()
		if not os.path.exists(self.date_path):
			os.makedirs(self.date_path)

		text_ = '爬虫%s启动, 收集%s%s的%s信息中......' % (self.name, self.city, self.type_, mode)
		print(text_)
		self.logger.info(text_)
		t0 = time.time()
		if mode == 'url':
			page_url_list = self._get_url_list_for_run(area, conditions)
			self.__run_for_urls(url_file, page_url_list)
			records = self.num_of_url_records
		else:
			self.__run_for_information(url_file, info_file)
			records = self.num_of_records
		dt = time.time() - t0
		text_ = '爬取结束, 成功采集%d条数据, 共耗时%.2f秒, 平均速度%.2f条/秒!'% (records, dt, records / dt)
		print(text_)
		self.logger.info(text_)

	@property
	def function_map(self):
		Maps = {'二手房': self.__get_info_in_per_url_ershoufang,
		        '新房': self.__get_info_in_per_url_loupan,
		        '成交': self.__get_info_in_per_url_chengjiao,
		        '租房': self.__get_info_in_per_url_zufang}

		return {self.TypesMap[i]: Maps[i] for i in ['二手房', '新房', '成交', '租房']}