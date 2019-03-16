#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JiaChengXu'
__mtime__ = '2019/3/11'
"""
from .BaseSpider import BaseSpider
from bs4 import BeautifulSoup
from .Config import MaxThread
import re
import threadpool
import os
import time


def NavigableString2str(nstring):
	ns = str(nstring).split()
	try:
		return ns[0]
	except:
		return ''

def StringClean(string):
	s = ''
	for si in string.split('\n'):
		for sii in si.split():
			s += sii + ' '
	return s[:-1]

class LianjiaSpider(BaseSpider):
	# TypesMap = {'二手房':'ershoufang', '新房':'loupan', '成交':'chengjiao', '租房':'zufang'}
	CityMap = {'苏州':'su', '上海':'sh', '南京':'nj'}
	Name = 'LianJia'
	LimitPages = 100

	def __init__(self, name='', file_path='./', city='苏州', types='二手房', pages=None):
		super(LianjiaSpider, self).__init__(name=self.Name + name,
		                                    filepath=file_path)
		self.pages = [pages if pages < self.LimitPages else self.LimitPages][0]
		if city in self.CityMap.keys():
			self.city = self.CityMap[city]
		else:
			self.logger.info('未知城市%s' % city)

		if types in self.TypesMap.keys():
			self.type_ = self.TypesMap[types]
		else:
			self.logger.info('未知形式%s' % types)


	def __get_info_in_per_url_chengjiao(self, soup):
		name = soup.select('.house-title')[0].text.split()[0]

		datail_1 = soup.select('p.record_detail')
		d1 = [n for n in re.findall("[0-9]*", datail_1[0].text) if n.__len__() > 0]
		price = soup.select('.info.fr i')[0].text
		information = [name, d1[0], '{0}-{1}-{2}'.format(d1[1], d1[2], d1[3]), price]

		detail_2 = soup.select('.deal-bread a')
		information += [detail_2[-2].text.split('二手房成交价格')[0], detail_2[-1].text.split('二手房成交价格')[0], ]

		detail_3 = soup.select('.info.fr span')[1:]
		information += [pi.contents[0].text for pi in detail_3]

		detail_4 = soup.select('.base li') + soup.select('.transaction li')
		information += [NavigableString2str(pi.contents[1]) for pi in detail_4]

		if self.title is None:
			self.title = ['屋名', '均价', '成交日期', '总价', '行政区', '行政子区'] + [NavigableString2str(pi.contents[1])
			                         for pi in detail_3] + [pi.contents[0].text for pi in detail_4]

		return information

	def __get_info_in_per_url_loupan(self, soup):
		detail_1 = soup.select('.fl.l-txt')
		information = [detail_1[0].contents[10].text, ]
		detail_2 = soup.select('.x-box li')
		information += [StringClean(pi.contents[3].text) for pi in detail_2[:-1]]

		if self.title is None:
			self.title =  ['楼盘名称', ] + [pi.contents[1].text[:-1] for pi in detail_2[:-1]]

		return information

	def __get_info_in_per_url_ershoufang(self, soup):
		detail_1 = soup.select('.aroundInfo')
		information = [detail_1[0].contents[0].contents[2].text, detail_1[0].contents[1].text[4:], ]
		information += [n for n in re.findall("[0-9]*", detail_1[0].contents[3].text) if n.__len__() > 0][0]

		detail_2 = soup.select('.price')
		information += [detail_2[0].contents[0].text, ]
		information += [n for n in re.findall("[0-9]*", detail_2[0].contents[2].text) if n.__len__() > 0][0]

		detail_3 = soup.select('.content li')[:20]
		information += [NavigableString2str(pi.contents[1]) for pi in detail_3[:12]]
		information += [StringClean(pi.contents[3].text) for pi in detail_3[12:]]

		if self.title is None:
			self.title = ['小区名称', '所在区域', '链家编号', '总价', '均价'] + [pi.contents[0].text
			                         for pi in detail_3[:12]] + [pi.contents[1].text for pi in detail_3[12:]]

		return information

	def __get_info_in_per_url_zufang(self, soup):
		detail_0_0 = soup.select('.bread__nav__wrapper')[0].text.split('\n')
		detail_0_0 = [d.split() for d in detail_0_0 if d > '']
		detail_0_0 = [d[0].split('租房')[0] for d in detail_0_0 if d]
		detail_0_1 = soup.select('.content__title')[0].text
		if detail_0_1.find('·') >= 0:
			detail_0_1 = detail_0_1.split()[2]
		else:
			detail_0_1 = detail_0_1.split()[0]
		information = [detail_0_0[1], detail_0_0[2], detail_0_1, ]

		detail_1 = soup.select('.content__subtitle')[0].text.split('\n')[1].split()
		detail_2 = soup.select('.content__aside--title')[0].text
		detail_3 = soup.select('.content__aside--tags')[0].text.replace('\n', ' ')
		information += [detail_1[0], detail_1[2], detail_1[3].split('：')[-1], detail_2, detail_3, ]

		detail_4 = soup.select('.content__article__table')[0].text.split('\n')
		information += [d for d in detail_4 if d > '']

		detail_5 = soup.select('.fl .oneline')[2:17]
		detail_5 = [d.text.split('：') for d in detail_5 if d.text.find('：') >= 0]
		information += [d[-1] for d in detail_5]

		if self.title is None:
			self.title =  ['行政区', '区域', '房名', '浏览次数', '上架时间', '房源编号', '价格', '标签', '租赁方式',
			                     '房型', '面积', '朝向'] + [d[0] for d in detail_5]
		return information

	def get_num_of_pages(self, url, types_):
		if types_ not in self.TypesMap.values():
			self.logger.info("Unknown %s! Set pages to 1" %types_)
			return 1

		html, ct = None, 0
		while html is None:
			html = self.grasp(url)
			ct += 1
			if ct > self.re_conncet:
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

		# url = 'https://su.lianjia.com/ershoufang/'
		# url = 'https://su.lianjia.com/chengjiao/'
		# url = 'https://su.lianjia.com/zufang/'
		# url = 'https://su.fang.lianjia.com/loupan/'

		original_url = 'https://%s.lianjia.com/%s/' % (self.city, self.type_)
		url_file = self.date_path + '/lianjia_page_urls_%s_%s' % (self.city, self.type_)
		info_file = self.date_path + "/lianjia_information_%s_%s" % (self.city, self.type_)
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

		## example_url = 'https://su.lianjia.com/ershoufang/xiangcheng/pg8a1/'
		page_url_list = []
		for i in range(1, pages + 1):
			temp = original_url
			if area is None and condtions is None:
				temp += 'pg%s/' % i
			elif area is None and condtions is not None:
				temp += 'pg%s%s/' % (i, condtions)
			elif area is not None and condtions is None:
				temp += '%s/pg%s/' % (area, i)
			else:
				temp += '%s/pg%s%s/' % (area, i, condtions)
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


# if __name__ == '__main__':
# 	bs = LianjiaSpider('spider_nj', './', city='南京', pages=1, types='成交')
# 	# url = 'https://su.lianjia.com/chengjiao/107100738802.html'
# 	# info = bs.get_info_in_per_url(url)
# 	bs.run()