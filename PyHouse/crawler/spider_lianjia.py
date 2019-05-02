#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JiaChengXu'
__mtime__ = '2019/3/11'
"""
from .spider_bases import BaseSpider
from bs4 import BeautifulSoup

class LianjiaSpider(BaseSpider):
	CityMap = {'苏州':'su', '上海':'sh', '南京':'nj'}
	Name = 'LianJia'
	LimitPages = 100
	TitleMap = {'二手房': ['行政区', '商圈', '小区', '链家编号', '总价', '均价', '户型', '楼层', '面积', '朝向', '装修',
	                    '产权年限', '挂牌日期', '交易属性', '上次交易', '房屋用途', '产权性质'],
	            '新房': ['行政区', '楼盘', '均价', '开发商', '绿化率', '容积率', '物业类型', '产权年限', '物业公司', '物业费'],
	            '成交': ['行政区', '商圈', '小区', '成交均价', '成交日期', '成交总价', '挂牌价格', '成交周期', '调价次数',
	                   '带看次数', '关注人数', '浏览次数', '户型', '楼层', '面积', '朝向', '年代', '装修', '产权年限',
	                   '链家编号', '交易属性', '挂牌日期',  '房屋用途', '产权性质'],
	            '租房': ['行政区', '商圈', '小区', '上架时间', '房源编号', '租金', '租赁方式', '户型', '面积', '朝向']}


	def __init__(self, name='', file_path='./', city='苏州', types='二手房', pages=None, re_connect=5):
		super(LianjiaSpider, self).__init__(name=self.Name + name, filepath = file_path, re_connect=re_connect)
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



	def __get_info_in_per_url_chengjiao(self, soup):
		detail_1 = soup.select('.wrapper .deal-bread a')
		detail_1 = [d.text.split('二手房成交价格')[0] for d in detail_1][-2:]

		name = soup.select('.house-title')[0].text.split()[0]

		detail_2 = soup.select('p.record_detail')[0].text.split(',')
		uprice = ''
		for i in filter(str.isdigit, detail_2[0]):
			uprice += i

		date = detail_2[-1].split('成交')[0]
		price = soup.select('.info.fr i')[0].text

		detail_3 = soup.select('.msg label')
		detail_3 = [d.text for d in detail_3]

		detail_4 = soup.select('.base li') + soup.select('.transaction li')
		detail_4 = [str(pi.contents[1]).split() for pi in detail_4]
		detail_4 = [d[0] for i, d in enumerate(detail_4) if i in [0, 1, 2, 6, 7, 8, 12, 14, 15, 16, 17, 19]]

		information = detail_1 + [name, uprice, date, price, ] + detail_3 + detail_4

		return information

	def __get_info_in_per_url_loupan(self, soup):
		detail_1 = soup.select('.fl.l-txt a')
		detail_1 = [d.text.split('楼盘')[0] for d in detail_1][3:-1]

		detail_2 = soup.select('.x-box li')
		detail_2 = [d.text.split('：') for d in detail_2]

		price = ''
		for i in filter(str.isdigit, detail_2[1][-1]):
			price += i

		kfs = detail_2[6][-1].split('\n')[1].split(',')[0]

		lh = detail_2[8][-1].split()[0]
		rj = detail_2[10][-1].split()[0]

		detail_2_2 = [detail_2[i][-1].split('\n')[1] for i in [12, 14, 16, 18]]

		information = detail_1 + [price, kfs, lh, rj] + detail_2_2

		return information

	def __get_info_in_per_url_ershoufang(self, soup):
		detail_1 = soup.select('.container .fl a')
		detail_1 = [d.text.split('二手房')[0] for d in detail_1][-3:]

		detail_2 = soup.select('.aroundInfo .houseRecord .info')[0].text
		ljlabel = ''
		for i in filter(str.isdigit, detail_2):
			ljlabel += i

		detail_3 = soup.select('.price .total')[0].text
		detail_4 = soup.select('.price .unitPriceValue')[0].text
		uprice = ''
		for i in filter(str.isdigit, detail_4):
			uprice += i

		detail_56 = soup.select('.content li')[:20]
		detail_5 = [str(d.contents[1]) for d in detail_56[:12]]
		detail_5 = [d for i, d in enumerate(detail_5) if i in [0, 1, 2, 6, 8, 11]]

		detail_6 = [d.text.split('\n') for d in detail_56[12:]]
		detail_6 = [d[2] for i, d in enumerate(detail_6) if i in [0, 1, 2, 3, 5]]

		information = detail_1 + [ljlabel, detail_3, uprice] + detail_5 + detail_6

		return information

	def __get_info_in_per_url_zufang(self, soup):
		detail_0_0 = soup.select('.bread__nav__wrapper')[0].text.split('\n')
		detail_0_0 = [d.split() for d in detail_0_0 if d > '']
		detail_0_0 = [d[0].split('租房')[0] for d in detail_0_0 if d][-2:]
		detail_0_1 = soup.select('.content__title')[0].text
		if detail_0_1.find('·') >= 0:
			detail_0_1 = detail_0_1.split()[2]
		else:
			detail_0_1 = detail_0_1.split()[0]

		detail_1 = soup.select('.content__subtitle')[0].text.split('\n')[1].split()
		detail_2 = soup.select('.content__aside--title')[0].text
		price = ''
		for i in filter(str.isdigit, detail_2):
			price += i

		detail_4 = soup.select('.content__article__table')[0].text.split('\n')
		detail_4 = [d for d in detail_4 if d > '']

		information = detail_0_0 + [detail_0_1, detail_1[2], detail_1[3].split('：')[-1], price, ] + detail_4

		return information

	def get_num_of_pages(self, url, types_):
		if types_ not in self.TypesMap.values():
			self.logger.info("Unknown %s! Set pages to 1" %types_)
			return 1

		html = self.grasp(url)
		if html is None:
			return 1

		soup = BeautifulSoup(html, "lxml")

		try:
			if types_ in [self.TypesMap[f] for f in ['成交', '二手房', ]]:
				records = int(soup.select('.total span')[0].text)
			elif types_ in [self.TypesMap['新房'], ]:
				records = int(soup.select('.resblock-have-find span')[1].text)
			else:
				records = int(soup.select('.content__title--hl')[0].text)
		except Exception as error_info:
			self.logger.info("Something is wrong! Set pages to 1")
			self.logger.error(error_info)
			return 1
		pages = int((int(records) - 1) / self.PerInPages[types_]) + 1
		return [pages if pages < self.LimitPages else self.LimitPages][0]

	def get_urls_in_per_url(self, url, type_='chengjiao'):
		select_key_map = dict(chengjiao='.listContent li a', ershoufang='.sellListContent li a',
		                      loupan='.resblock-name a', zufang='.content__list--item--main a')
		if type_ in select_key_map:
			select_key = select_key_map[type_]
		else:
			self.logger.info('未知形式%s' % type_)
			return []

		try:
			data = self.grasp(url)
			soup = BeautifulSoup(data, 'html.parser')
			url_info = soup.select(select_key)
			page_url = [pg_url['href'] for pg_url in url_info]
			if type_ in ['chengjiao', 'ershoufang']:
				urls = [f for f in list(set(page_url)) if f.find('.html') >= 0]
			elif type_ in ['loupan', ]:
				origin_url = 'https://%s.lianjia.com/' % self.city
				urls = [origin_url + f + 'xiangqing/' for f in list(set(page_url))]
			else:
				origin_url = 'https://%s.lianjia.com/' % self.city
				urls = [origin_url + f  for f in list(set(page_url)) if f.find('.html') >= 0]

		except Exception as error_info:
			urls = []
			self.logger.error(error_info)
		return urls

	def _get_url_list_for_run(self, area=None, conditions=None):
		# url = 'https://su.lianjia.com/ershoufang/'
		# url = 'https://su.lianjia.com/chengjiao/'
		# url = 'https://su.lianjia.com/zufang/'
		# url = 'https://su.fang.lianjia.com/loupan/'
		if self.type_ in [self.TypesMap[f] for f in ['成交', '二手房', '租房']]:
			original_url = 'https://%s.lianjia.com/%s/' % (self.city, self.type_)
		else:
			original_url = 'https://%s.fang.lianjia.com/%s/' % (self.city, self.type_)

		temp = original_url
		if area is not None:
			temp += '%s/' % area
		if conditions is not None:
			temp += '%s/' % conditions

		if self.pages is None:
			pages = self.get_num_of_pages(temp, self.type_)
		else:
			pages = self.pages

		## example_url = 'https://su.lianjia.com/ershoufang/xiangcheng/pg8a1/'
		page_url_list = []
		for i in range(1, pages + 1):
			temp = original_url
			if area is None and conditions is None:
				temp += 'pg%s/' % i
			elif area is None and conditions is not None:
				temp += 'pg%s%s/' % (i, conditions)
			elif area is not None and conditions is None:
				temp += '%s/pg%s/' % (area, i)
			else:
				temp += '%s/pg%s%s/' % (area, i, conditions)
			page_url_list += [temp, ]

		return page_url_list

	def _get_save_file_name(self):
		url_file = self.date_path + '/lianjia_urls_%s_%s.txt' % (self.city, self.type_)
		info_file = self.date_path + "/lianjia_information_%s_%s.csv" % (self.city, self.type_)
		return url_file, info_file


	@property
	def function_map(self):
		return {k: v for k, v in zip(self.TypesMap.values(), [self.__get_info_in_per_url_ershoufang,
				                                              self.__get_info_in_per_url_loupan,
				                                              self.__get_info_in_per_url_chengjiao,
				                                              self.__get_info_in_per_url_zufang])}


# if __name__ == '__main__':
# 	bs = LianjiaSpider('spider_nj', './', city='南京', pages=1, types='成交')
# 	# url = 'https://su.lianjia.com/chengjiao/107100738802.html'
# 	# info = bs.get_info_in_per_url(url)
# 	bs.run()