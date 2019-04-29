#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JiaChengXu'
__mtime__ = '2019/3/25'
"""
from .BaseSpider import BaseSpider
from bs4 import BeautifulSoup
from .Config import *
import threadpool



class FivekSpider(BaseSpider):
	TypesMap = {'二手房': 'sell', '新房': 'new', '小区': 'community', '租房': 'rent'}
	PerInPages = {k: v for k, v in zip(TypesMap.values(), [25, ] * 4)}
	CityMap = {'常熟':'cs', }
	Name = '5khouse'
	LimitPages = 30
	TitleMap = {'二手房': ['行政区', '商圈', '总价', '均价', '小区', '户型', '面积', '朝向', '楼层', '类型', '装修',
	                    '房源编号', '更新日期'],
	            '新房': ['行政区', '楼盘', '均价', '开发商', '绿化率', '容积率', '物业类型', '产权年限', '物业公司', '物业费'],
	            '小区': ['行政区', '商圈', '小区', '成交均价', '成交日期', '成交总价', '挂牌价格', '成交周期', '调价次数',
	                   '带看次数', '关注人数', '浏览次数', '户型', '楼层', '面积', '朝向', '年代', '装修', '产权年限',
	                   '链家编号', '交易属性', '挂牌日期',  '房屋用途', '产权性质'],
	            '租房': ['行政区', '商圈', '小区', '上架时间', '房源编号', '租金', '租赁方式', '户型', '面积', '朝向']}


	def __init__(self, name='', file_path='./', city='常熟', types='二手房', pages=None, re_connect=5):
		super(FivekSpider, self).__init__(name=self.Name + name, filepath = file_path, re_connect=re_connect)
		if pages is not None:
			self.pages = [pages if pages < self.LimitPages else self.LimitPages][0]
		else:
			self.pages = pages
		if city in self.CityMap.keys():
			self.city = self.CityMap[city]
		else:
			self.logger.info('初始化时, 未知城市%s' % city)

		if types in self.TypesMap.keys():
			self.title = self.TitleMap[types]
			self.type_ = self.TypesMap[types]
		else:
			self.logger.info('初始化时,未知形式%s' % types)


	def __get_info_in_per_url_ershoufang(self, soup):
		detail_0 = soup.select('.nav a')
		detail_0 = [d.text.split('二手房')[0] for d in detail_0][-2:]

		detail_1 = soup.select('.rr dt')
		detail_1 = [d.text.split('：') for d in detail_1]

		total_price, unit_price, area = '', '', ''
		for i in detail_1:
			if '售价' in i[0]:
				prices = i[1].split('（')
				for s in filter(str.isdigit, prices[0]):
					total_price += s
				for s in filter(str.isdigit, prices[1].split('.')[0]):
					unit_price += s

			if '小区' in i[0]:
				area = i[1].split(' ( ')[0]

		detail_2 = soup.select('.rr dd')[:6]
		detail_2 = [d.text.split('：') for d in detail_2]
		detail_2_1 = [d[0] for d in detail_2]
		detail_2_2 = [d[1] for d in detail_2]

		d_2 = ['', ] * 6
		for i, key in enumerate(['户型', '建筑面积', '朝向', '所在楼层', '房屋类型', '装修情况']):
			if key in detail_2_1:
				idx = detail_2_1.index(key)
				d_2[i] = detail_2_2[idx]

		detail_3 = soup.select('.bh')[0].text.split()
		detail_3 = [d.split('：')[-1] for d in detail_3][:2]

		information = detail_0 + [total_price, unit_price, area] + d_2 + detail_3

		if sum(len(f) for f in information) <= 0:
			information = []

		return information

	def __get_info_in_per_url_loupan(self, soup):
		pass

	def __get_info_in_per_url_zufang(self, soup):
		pass

	def __get_info_in_per_url_chengjiao(self, soup):
		pass

	def get_num_of_pages(self, url, modes=True):
		html = self.grasp(url)
		if html is None:
			return 1

		soup = BeautifulSoup(html, "lxml")

		try:
			if modes:
				pages = soup.select('.tj')[0].text.split('/')[-1]
				pages = int(pages)
			else:
				records = soup.select('.zongnum')[0].text
				pages = ''
				for s in filter(str.isdigit, records):
					pages += s
				pages = int((int(pages) - 1) / 25) + 1

		except Exception as error_info:
			self.logger.info("Something is wrong! Set pages to 1")
			self.logger.error(error_info)
			return 1

		return [pages if pages < self.LimitPages else self.LimitPages][0]

	def get_urls_in_per_url(self, url, type_='sell'):
		select_key_map = dict(community='.infobox dl dt a', sell='.house dt a',
		                      new='.resblock-name a', rent='.house dt a')
		if type_ in select_key_map:
			select_key = select_key_map[type_]
		else:
			self.logger.info('未知形式%s' % type_)
			return []

		try:
			data = self.grasp(url)
			soup = BeautifulSoup(data, 'html.parser')
			url_info = soup.select(select_key)
			page_url = list(set([pg_url['href'] for pg_url in url_info]))
			if type_ in ['sell']:
				urls = [f for f in page_url if f.find('selldetail') >= 0]
			elif type_ in ['community']:
				sellurls = [f for f in page_url if f.find('communityselllist') >= 0]
				renturls = [f for f in page_url if f.find('communityrentlist') >= 0]
				urls = sellurls + renturls
			else:
				urls = []
		except Exception as error_info:
			urls = []
			self.logger.error(error_info)
		return urls


	def __get_url_list_for_run_community(self, area=None, conditions=None):
		if area is None:
			area = '-a4'
		if conditions is None:
			conditions = '-b-k5-p-w-t'

		original_url = 'http://cs.5khouse.com/community/communitylist_%s%s.aspx' %(area, conditions)

		if self.pages is None:
			pages = self.get_num_of_pages(original_url, modes=True)
		else:
			pages = self.pages

		original_urls = original_url.split('p-')
		page_url_list = []
		for i in range(1, pages + 1):
			temp = original_urls[0] + 'p' + str(i) + '-' + original_urls[1]
			page_url_list += [temp, ]
		return page_url_list


	def __collect_page_of_urls(self, url, extends):
		if self.pages is None:
			pages = self.get_num_of_pages(url, modes=False)
		else:
			pages = self.pages

		for i in range(1, pages + 1):
			temp = url[:-5] + extends + str(i) + '.aspx'
			self.mutex.acquire()
			self.link_file.write(temp + '\n')
			self.mutex.release()


	def run_from_community(self):

		keywords = 'selllist' if self.type_ == 'sell' else 'rentlist'
		extends = '-b-c-p' if self.type_ == 'sell' else '-b-c-d-p2'

		with open(self.date_path + '/5khouse_urls_%s_community.txt' % self.city, 'rb') as file:
			lines = file.readlines()
		urls = [line.decode().split('\ufeff')[-1].split('\r')[0] for line in lines]
		urls = [f for f in list(set(urls)) if f.find(keywords) >= 0]

		with open(self.date_path + '/5khouse_pageurls_%s_%s.txt' % (self.city, self.type_),
		          'w+', encoding='utf-8-sig') as self.link_file:
			arg = zip(zip(urls, [extends, ] * len(urls)), [None, ] * len(urls))
			pool = threadpool.ThreadPool(MaxThread)
			my_requests = threadpool.makeRequests(self. __collect_page_of_urls, arg)
			[pool.putRequest(req) for req in my_requests]
			pool.wait()
			pool.dismissWorkers(MaxThread, do_join=True)  # 完成后退出



	def _get_url_list_for_run(self, area=None, conditions=None):
		if self.type_ == self.TypesMap['小区']:
			return self.__get_url_list_for_run_community(area, conditions)

		keywords = 'selllist' if self.type_ == 'sell' else 'rentlist'

		with open(self.date_path + '/5khouse_pageurls_%s_%s.txt' % (self.city, self.type_), 'rb') as file:
			lines = file.readlines()
		urls = [line.decode().split('\ufeff')[-1].split('\r')[0] for line in lines]
		page_url_list = [f for f in list(set(urls)) if f.find(keywords) >= 0]
		return page_url_list

	def _get_save_file_name(self):
		url_file = self.date_path + '/5khouse_urls_%s_%s.txt' % (self.city, self.type_)
		info_file = self.date_path + "/5khouse_information_%s_%s.csv" % (self.city, self.type_)
		return url_file, info_file






	@property
	def function_map(self):
		return {k: v for k, v in zip(self.TypesMap.values(), [self.__get_info_in_per_url_ershoufang,
				                                              self.__get_info_in_per_url_loupan,
				                                              self.__get_info_in_per_url_chengjiao,
				                                              self.__get_info_in_per_url_zufang])}