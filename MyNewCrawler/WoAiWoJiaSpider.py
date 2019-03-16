#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JiaChengXu'
__mtime__ = '2019/3/15'
"""

from .BaseSpider import BaseSpider
from bs4 import BeautifulSoup
from .Config import MaxThread
import re
import threadpool
import os
import time

class WoAiWoJiaSpider(BaseSpider):
	TypesMap = {'二手房': 'ershoufang', '新房': 'loupan', '成交': 'solds', '租房': 'zufang'}
	CityMap = {'苏州':'sz', }
	Name = '5i5j'
	PerInPages = {k: v for k, v in zip(TypesMap.values(), [30, 10, 30, 30])}

	def __init__(self, name='', file_path='./', city='苏州',types='二手房', pages=None):
		super(WoAiWoJiaSpider, self).__init__(name=self.Name + name, filepath=file_path)
		self.pages = pages
		if city in self.CityMap.keys():
			self.city = self.CityMap[city]
		else:
			self.logger.info('未知城市%s' % city)

		if types in self.TypesMap.keys():
			self.type_ = self.TypesMap[types]
		else:
			self.logger.info('未知形式%s' % types)


	def __get_info_in_per_url_ershoufang(self, soup):
		detail_1 = soup.select('.housesty .jlinfo')
		detail_1 = [d.text for d in detail_1]
		information = detail_1

		detail_2 = soup.select('.zushous li')
		detail_2 = [d.text.split('\n')[0].split('：') for d in detail_2]
		information += [d[-1] for d in detail_2]

		detail_3 = soup.select('.infocon span')[3].text
		information += [detail_3, ]

		if self.title is None:
			self.title = ['总价', '均价', '户型', '面积'] + [d[0] for d in detail_2] + ['产权性质', ]

		return information

	def __get_info_in_per_url_chengjiao(self, soup):
		detail_1 = soup.select('.house-tit')
		detail_1 = [d.text.split() for d in detail_1]
		information = detail_1[0]

		detail_2 = soup.select('.house-info .cjinfo')
		detail_2 = [d.text for d in detail_2]
		information += detail_2[:-1] + [d for d in detail_2[-1].split() if len(d) > 8]

		detail_3 = soup.select('.detailinfo li')
		detail_3 = [d.text.split('：') for d in detail_3]
		information += [d[-1] for d in detail_3]

		detail_4 = soup.select('.infomain li')[-3].text.split('所在商圈')[-1]
		information += [detail_4, ]

		if self.title is None:
			self.title =  ['户名', '户型', '总价', '均价', '成交日期'] + [d[0] for d in detail_3] + ['商圈', ]
		return information

	def __get_info_in_per_url_loupan(self, soup):
		detail_0 = soup.select('.name')[0].text
		detail_1 = soup.select('.details_price  .clearfix')[0].text.split()[0]
		information = [detail_0, detail_1, ]

		detail_2 = soup.select('.clearfix .details_date .clearfix')
		detail_2 = [[d1 for d1 in d.text.split('\n') if d1 > ''] for d in detail_2][:2]
		information += [d[1] for d in detail_2]

		detail_3 = soup.select('.style_list  .txtList p')
		detail_3 = [d.text for d in detail_3]

		detail_4 = soup.select('.style_list  .txtList .txt')
		detail_4 = [d.text for d in detail_4][1:8]
		information += detail_3 + detail_4


		if self.title is None:
			self.title = ['楼盘名', '均价', ] + [d[0] for d in detail_2] + ['核心卖点', '售楼处', '交房时间',
			                     '销售状态', '产权年限', '建筑面积', '建筑类别', '绿化率', '容积率']
		return information

	def __get_info_in_per_url_zufang(self, soup):
		detail_1 = soup.select('.housesty .jlinfo')
		detail_1 = [d.text for d in detail_1]

		detail_2 = soup.select('.zushous li')
		detail_2 = [d.text.split('：') for d in detail_2]

		information = detail_1 + [d[-1] for d in detail_2]

		if self.title is None:
			self.title = ['租金', '户型', '面积', '支付方式'] + [d[0] for d in detail_2]
		return information

	def get_urls_in_per_url(self, url, type_='chengjiao'):
		select_key_map = dict(chengjiao='.pList li a', ershoufang='.pList li .listTit a',
		                      loupan='.houseList_list .txt1 a', zufang='.pList li .listTit a')
		if type_ in select_key_map:
			select_key = select_key_map[type_]
		else:
			self.logger.info('未知形式%s' % type_)
			return []

		try:
			data = self.grasp(url)
			soup = BeautifulSoup(data, 'lxml')
			url_info = soup.select(select_key)
			page_url = [pg_url['href'] for pg_url in url_info]
			if type_ in [self.TypesMap[f] for f in ['成交', '二手房', '租房']]:
				origin_url = 'https://%s.5i5j.com' % self.city
			else:
				origin_url = 'https://fang.5i5j.com'
			urls = [origin_url + f for f in list(set(page_url))]
		except Exception as error_info:
			urls = []
			self.logger.error(error_info)
		return urls

	def get_num_of_pages(self, url, types_):
		if types_ not in self.TypesMap.values():
			self.logger.info("Unknown %s! Set pages to 1" % types_)
			return 1

		html, ct = None, 0
		while html is None:
			html = self.grasp(url)
			ct += 1
			if ct > self.re_conncet:
				return 1

		soup = BeautifulSoup(html, 'lxml')
		try:
			if types_ in [self.TypesMap[f] for f in ['成交', '二手房', '租房']]:
				records = soup.select('.total-box span')[0].text
			else:
				records = soup.select('.houseList_total i')[0].text
		except Exception as error_info :
			self.logger.info("Something is wrong! Set pages to 1")
			self.logger.error(error_info)
			return 1
		pages = int((int(records) - 1) / self.PerInPages[types_]) + 1
		return [pages if pages < self.LimitPages else self.LimitPages][0]

	def __collect_and_save_urls(self, url):
		urls, ct = [], 0
		while not urls:
			urls = self.get_urls_in_per_url(url, self.type_)
			ct += 1
			if ct >= self.re_conncet:
				break
		if urls:
			for u in urls:
				if u:
					self.mutex.acquire()
					self.url_file.write(u + '\n')
					self.mutex.release()

	def __collect_and_save_info_in_per_url(self, url):
		info, ct = [], 0
		while not info:
			info = self.get_info_in_per_url(url, self.type_)
			ct += 1
			if ct >= self.re_conncet:
				break
		if info:
			self.mutex.acquire()
			self.info_file.write(self.date_string + "," + info + "\n")
			self.num_of_records += 1
			self.mutex.release()


	def run(self, area=None, condtions=None,):
		print('爬虫%s启动, 收集%s%s信息中......' % (self.name, self.city, self.type_))
		t0 = time.time()
		if not os.path.exists(self.date_path):
			os.makedirs(self.date_path)

		# url = 'https://sz.5i5j.com/solds/'
		# url = 'https://sz.5i5j.com/ershoufang/'
		# url = 'https://sz.5i5j.com/zufang/'
		# url = 'https://fang.5i5j.com/sz/loupan/'

		if self.type_ in [self.TypesMap[f] for f in ['成交', '二手房', '租房']]:
			original_url = 'https://%s.5i5j.com/%s/' % (self.city, self.type_)
		else:
			original_url = 'https://fang.5i5j.com/%s/%s/' % (self.city, self.type_)


		url_file = self.date_path + '/5i5j_page_urls_%s_%s' % (self.city, self.type_)
		info_file = self.date_path + "/5i5j_information_%s_%s" % (self.city, self.type_)
		temp = original_url
		if area is not None:
			temp += '%s/' % area
			url_file += '_%s' % area
			info_file += '_%s' % area
		if condtions is not None:
			temp += '%s/' % condtions
			url_file += '_%s' % condtions
			info_file += '_%s' % condtions
		url_file += '.txt'
		info_file += '.csv'

		if self.pages is None:
			pages = self.get_num_of_pages(temp, self.type_)
		else:
			pages = self.pages

		## example_url = 'https://sz.5i5j.com/ershoufang/xiangchengqu/a4p5n3/'
		page_url_list = []
		for i in range(1, pages + 1):
			temp = original_url
			if area is None and condtions is None:
				temp += 'n%s/' % i
			elif area is None and condtions is not None:
				temp += '%sn%s/' % (condtions, i)
			elif area is not None and condtions is None:
				temp += '%s/n%s/' % (area, i)
			else:
				temp += '%s/%sn%s/' % (area, condtions, i)
			page_url_list += [temp, ]

		if not os.path.exists(url_file):
			with open(url_file, 'w+', encoding='utf-8-sig') as self.url_file:
				arg = zip(zip(page_url_list), [None, ] * pages)

				pool = threadpool.ThreadPool(MaxThread)
				my_requests = threadpool.makeRequests(self.__collect_and_save_urls, arg)
				[pool.putRequest(req) for req in my_requests]
				pool.wait()
				pool.dismissWorkers(MaxThread, do_join=True)  # 完成后退出

		with open(url_file, 'rb') as file:
			lines = file.readlines()

		with open(info_file, 'w+', encoding='utf-8-sig') as self.info_file:
			urls = [line.decode().split('\ufeff')[-1].split('\r')[0] for line in lines]
			arg = zip(zip(urls), [None, ] * len(urls))
			pool = threadpool.ThreadPool(MaxThread)
			my_requests = threadpool.makeRequests(self.__collect_and_save_info_in_per_url, arg)
			[pool.putRequest(req) for req in my_requests]
			pool.wait()
			pool.dismissWorkers(MaxThread, do_join=True)  # 完成后退出
			self.info_file.write("采集时间," + self.title + "\n")

		dt = time.time() - t0
		text_ = '爬取结束, 成功采集%d条数据, 共耗时%.2f秒, 平均速度%d条/秒!'% (self.num_of_records,
		                                                        dt,
		                                                        self.num_of_records / dt)
		print(text_)
		self.logger.info(text_)


	@property
	def function_map(self):
		return {k: v for k, v in zip(self.TypesMap.values(), [self.__get_info_in_per_url_ershoufang,
				                                              self.__get_info_in_per_url_loupan,
				                                              self.__get_info_in_per_url_chengjiao,
				                                              self.__get_info_in_per_url_zufang])}
