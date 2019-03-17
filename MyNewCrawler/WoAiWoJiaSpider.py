#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JiaChengXu'
__mtime__ = '2019/3/15'
"""

from .BaseSpider import BaseSpider
from bs4 import BeautifulSoup

class WoAiWoJiaSpider(BaseSpider):
	TypesMap = {'二手房': 'ershoufang', '新房': 'loupan', '成交': 'solds', '租房': 'zufang'}
	CityMap = {'苏州':'sz', }
	Name = '5i5j'
	PerInPages = {k: v for k, v in zip(TypesMap.values(), [30, 10, 30, 30])}
	TitleMap = {'二手房': ['房源ID', '行政区', '商圈', '小区', '总价', '单价', '户型', '面积', '楼层', '产权', '年代'],
	            '新房': ['行政区', '楼盘', '均价', '开发商', '交房时间', '销售状态', '产权年限',  '绿化率', '容积率'],
	            '成交': ['小区', '户型', '总价', '均价', '成交日期', '楼层', '朝向', '商圈'],
	            '租房': ['租金', '户型', '面积', '支付方式', '年代', '出租方式', '行政区', '商圈', '小区']}

	def __init__(self, name='', file_path='./', city='苏州',types='二手房', pages=None):
		super(WoAiWoJiaSpider, self).__init__(name=self.Name + name, filepath=file_path)
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
		detail_0 = soup.select('.rent-top p')[0].text.split('房源ID：')[-1]

		detail_1 = soup.select('.cur-path a')
		detail_1 = [d.text.split('二手房')[0] for d in detail_1][-3:]

		detail_2 = soup.select('.housesty .jlinfo')
		detail_2 = [d.text for d in detail_2]

		detail_3 = soup.select('.infocon span')
		detail_3 = [d.text for i, d in enumerate(detail_3) if i in [1, 3, 4]]

		information = [detail_0, ] + detail_1 + detail_2 + detail_3

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
		information += [d[-1] for d in detail_3][:2]

		detail_4 = soup.select('.infomain li')
		detail_4 = [d.text.split('所在商圈')[-1] for d in detail_4 if d.text.find('所在商圈') >= 0]
		information += detail_4

		return information

	def __get_info_in_per_url_loupan(self, soup):
		detail_0 = soup.select('.menu li')
		detail_0 = [d.text.split('楼盘')[0] for d in detail_0][-2:]

		detail_1 = soup.select('.details_price  .clearfix')[0].text.split()[0]
		price = ''
		for i in filter(str.isdigit, detail_1):
			price += i

		detail_2 = soup.select('.style_list  .txtList .txt')
		detail_2 = [d.text for d in detail_2]
		wy = detail_2[0].split()[0]
		d2 = [d for i, d in enumerate(detail_2) if i in [1, 2, 3, 6, 7]]

		information = detail_0 + [price, wy] + d2

		return information

	def __get_info_in_per_url_zufang(self, soup):
		detail_1 = soup.select('.housesty .jlinfo')
		detail_1 = [d.text for d in detail_1]

		detail_2 = soup.select('.zushous li')
		d2 = ['', '']
		for d in detail_2:
			if d.text.find('年代') >= 0:
				d2[0] = d.text.split('：')[-1]
			if d.text.find('出租方式') >= 0:
				d2[1] = d.text.split('：')[-1]

		detail_3 = soup.select('.cur-path a')
		detail_3 = [d.text.split('租房')[0] for d in detail_3][-3:]

		information = detail_1 + d2 + detail_3

		return information

	def get_urls_in_per_url(self, url, type_='solds'):
		select_key_map = {k: v for k, v in zip(self.TypesMap.values(), ['.pList li .listTit a',
		                  '.houseList_list .txt1 a','.pList li a','.pList li .listTit a'])}

		if type_ in select_key_map.keys():
			select_key = select_key_map[type_]
		else:
			self.logger.info('采集网页时，未知形式%s' % type_)
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

	def _get_url_list_for_run(self, area=None, conditions=None):
		if self.type_ in [self.TypesMap[f] for f in ['成交', '二手房', '租房']]:
			original_url = 'https://%s.5i5j.com/%s/' % (self.city, self.type_)
		else:
			original_url = 'https://fang.5i5j.com/%s/%s/' % (self.city, self.type_)

		# url = 'https://sz.5i5j.com/solds/'
		# url = 'https://sz.5i5j.com/ershoufang/'
		# url = 'https://sz.5i5j.com/zufang/'
		# url = 'https://fang.5i5j.com/sz/loupan/'

		temp = original_url
		if area is not None:
			temp += '%s/' % area
		if conditions is not None:
			temp += '%s/' % conditions


		if self.pages is None:
			pages = self.get_num_of_pages(temp, self.type_)
		else:
			pages = self.pages

		## example_url = 'https://sz.5i5j.com/ershoufang/xiangchengqu/a4p5n3/'
		page_url_list = []
		for i in range(1, pages + 1):
			temp = original_url
			if area is None and conditions is None:
				temp += 'n%s/' % i
			elif area is None and conditions is not None:
				temp += '%sn%s/' % (conditions, i)
			elif area is not None and conditions is None:
				temp += '%s/n%s/' % (area, i)
			else:
				temp += '%s/%sn%s/' % (area, conditions, i)
			page_url_list += [temp, ]

		return page_url_list

	def _get_save_file_name(self):
		url_file = self.date_path + '/5i5j_page_urls_%s_%s.txt' % (self.city, self.type_)
		info_file = self.date_path + "/5i5j_information_%s_%s.csv" % (self.city, self.type_)
		return url_file, info_file


	@property
	def function_map(self):
		Maps = {'二手房': self.__get_info_in_per_url_ershoufang,
		        '新房': self.__get_info_in_per_url_loupan,
		        '成交': self.__get_info_in_per_url_chengjiao,
		        '租房': self.__get_info_in_per_url_zufang}

		return {self.TypesMap[i]: Maps[i] for i in ['二手房', '新房', '成交', '租房']}
