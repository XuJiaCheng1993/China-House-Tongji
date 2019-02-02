#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JiaChengXu'
__mtime__ = '2019/1/29'
"""

import urllib3
import requests
import Config
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from tqdm import tqdm
import re
import time
import os
import pandas as pd
import gc

LianJiaMap = {'苏州大市':None,
              '昆山':'kunshan',
              '高新':'gaoxing1',
              '吴中':'wuzhong',
              '相城':'xiangcheng',
              '吴江':'wujiang',
              '工业园区':'gongyeyuan',
              '姑苏':'gusu'}

def grasp(url, method='selenium', is_agent=False, save_name='None', timeout=5):
	if method in ['selenium', ]:
		if is_agent:
			from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
			dcap = dict(DesiredCapabilities.PHANTOMJS)
			dcap['phantomjs.page.settings.userAgent'] = (random.choice(Config.UserAgents))
			driver = webdriver.PhantomJS(
				executable_path=r'D:\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\bin\phantomjs.exe',
				desired_capabilities=dcap,
			)
		else:
			driver = webdriver.PhantomJS(
				executable_path=r'D:\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\bin\phantomjs.exe')
		try:
			driver.get(url)  # 加载网页
			driver.save_screenshot(save_name + '.png')
			data = driver.page_source  # 获取网页文本
		except Exception as e:
			data = None
			print(e)
		driver.quit()

	elif method in ['urllib3', ]:
		if is_agent:
			headers = {'User-Agent' : random.choice(Config.UserAgents)}
		else:
			headers = {}
		try:
			http = urllib3.PoolManager()
			res = http.request('GET', url, headers=headers)
			data = res.data
		except Exception as e:
			data = None
			print(e)

	elif method in ['requests', ]:
		if is_agent:
			headers = {'User-Agent' : random.choice(Config.UserAgents)}
		else:
			headers = {}
		try:
			res = requests.get(url, headers=headers, timeout=timeout)
			data = res.text
		except Exception as e:
			data = None
			# print(e)
	else:
		data = None

	return data

def daily_info():
	url = 'https://su.lianjia.com/fangjia/'
	# bs提取内容
	soup = BeautifulSoup(grasp(url), "lxml")
	price = soup.select('.num')
	name = soup.select('.name')

	# 整合数据
	price = [h.text.split()[0] for h in price]
	name = ['苏州', '新增房', '新增房', '带看量'] + [h.text.split()[0] for h in name]
	daily = {name[i] : int(price[i]) for i in range(price.__len__())}

	return daily

def NavigableString2str(nstring):
	ns = str(nstring).split()
	try:
		return ns[0]
	except:
		return ''

def str_regular(string):
	s = ''
	for si	in string.split('\n'):
		for sii in si.split():
			s += sii + ' '
	return s[:-1]

def crawler_sleep():
	time.sleep(0.2 * random.random() + 0.1)

def _get_info_in_per_url_loupan(soup):
	name = soup.select('.fl.l-txt')
	inform = {'楼盘名称':name[0].contents[10].text}

	house_info = soup.select('.x-box li')
	house_dict =  {pi.contents[1].text[:-1]: str_regular(pi.contents[3].text)
				   for pi in house_info[:-1]}

	inform = dict(inform, **house_dict)
	return inform

def _get_info_in_per_url_ershoufang(soup):
	inform = {}

	around_info = soup.select('.aroundInfo')
	inform['小区名称'] = around_info[0].contents[0].contents[2].text
	inform['所在区域'] = around_info[0].contents[1].text[4:]
	inform['链家编号'] = [n for n in re.findall("[0-9]*", around_info[0].contents[3].text) if n.__len__() > 0][0]

	price_info = soup.select('.price')
	inform['总价'] = price_info[0].contents[0].text
	inform['均价'] = [n for n in re.findall("[0-9]*", price_info[0].contents[2].text) if n.__len__() > 0][0]

	house_info = soup.select('.content li')[:20]
	house_dict = dict({pi.contents[0].text: NavigableString2str(pi.contents[1]) for pi in house_info[:12]},
	                  **{pi.contents[1].text: str_regular(pi.contents[3].text) for pi in house_info[12:]})

	inform = dict(inform, **house_dict)
	return inform

def _get_info_in_per_url_chengjiao(soup):
	# 房屋名 成交日期 均价 总价
	house_title = soup.select('.house-title')[0].text.split()[0]

	record_datail = soup.select('p.record_detail')
	record_number = [n for n in re.findall("[0-9]*", record_datail[0].text) if n.__len__() > 0]

	price = soup.select('.info.fr i')[0].text
	inform = {'屋名': house_title,
	          '均价': record_number[0],
	          '成交日期': '{0}-{1}-{2}'.format(record_number[1], record_number[2], record_number[3]),
	          '总价': price,
	          }

	# 成交信息
	price_info = soup.select('.info.fr span')[1:]
	price_dict = {NavigableString2str(pi.contents[1]): pi.contents[0].text
	              for pi in price_info}
	inform = dict(inform, **price_dict)

	# 房屋信息
	house_base_info = soup.select('.base li')
	house_transaction_info = soup.select('.transaction li')
	house_dict = {pi.contents[0].text: NavigableString2str(pi.contents[1])
	              for pi in house_base_info + house_transaction_info}

	inform = dict(inform, **house_dict)
	return inform

def get_info_in_per_url(url, type='chengjiao', verbose=False):
	data = grasp(url, method='requests', is_agent=True)
	if data is None:
		inform =  {}
	else:
		soup = BeautifulSoup(data, 'html.parser')
		if type == 'chengjiao':
			try:
				inform = _get_info_in_per_url_chengjiao(soup)
			except Exception as e:
				inform = {}
				if verbose:
					print(e)
		elif type == 'ershoufang':
			try:
				inform = _get_info_in_per_url_ershoufang(soup)
			except Exception as e:
				inform = {}
				if verbose:
					print(e)
		elif type == 'loupan':
			try:
				inform = _get_info_in_per_url_loupan(soup)
			except Exception as e:
				inform = {}
				if verbose:
					print(e)
		else:
			inform = {}
	return inform

def get_urls_in_per_url(url, type='chengjiao', verbose=False):
	if type == 'chengjiao':
		select_key = '.listContent li a'
	elif type == 'ershoufang':
		select_key = '.sellListContent li a'
	elif type == 'loupan':
		select_key = '.resblock-name a'
	else:
		return []

	try:
		data = grasp(url, method='requests', is_agent=True)
		soup = BeautifulSoup(data, 'html.parser')
		url_info =  soup.select(select_key)
		page_url = [pg_url['href'] for pg_url in url_info]
		if type in ['chengjiao', 'ershoufang']:
			urls = [f for f in list(set(page_url)) if f.find('.html') >=0]
		elif type in ['loupan', ]:
			origin_url = 'https://su.lianjia.com/'
			urls = [origin_url + f + 'xiangqing/' for f in list(set(page_url))]
		else:
			urls = []
	except Exception as e:
		urls = []
		if verbose:
			print(e)
	return urls

def get_district_information(district='kunshan', area=None, type='chengjiao', maxpage=100, attemp_times=5, verbose=False):
	origin_url = 'https://su.lianjia.com/'

	try:
		dist = LianJiaMap[district]
		if dist is None:
			dist = 'pg'
		else:
			dist += '/pg'
	except Exception as e:
		print(e)
		return [], []

	if area is None:
		suffix = '/'
	else:
		suffix = area.lower() + '/'

	urls = []
	for i in tqdm(range(maxpage), desc='提取{0}{1}网页链接'.format(district, type)):
		url = origin_url + type + '/' + dist + str(i + 1) + suffix
		page_url = []
		ct = 0
		while not page_url:
			page_url = get_urls_in_per_url(url, type, verbose)
			ct += 1
			if ct >= attemp_times:
				break
		crawler_sleep()
		if not page_url:
			break
		page_url = list(set(page_url))
		urls += page_url


	informs = []
	failed_ulr = []
	for i in tqdm(iterable=range(urls.__len__()), desc='提取{0}{1}网页信息'.format(district, type)):
		tmp = []
		ct = 0
		while not tmp:
			tmp = get_info_in_per_url(urls[i], type, verbose)
			ct += 1
			if ct >= attemp_times:
				break
		crawler_sleep()
		if tmp:
			informs.append(tmp)
		else:
			failed_ulr.append(urls[i])

	gc.collect()

	return informs, failed_ulr


def LianjiaTotal(dist_name, dist_area, type, file_path, attemp_times=10):

	nums = dist_name.__len__()

	for i in range(nums):
		dn = LianJiaMap[dist_name[i]]
		if dn is None:
			dn = 'suzhou'
		if dist_area[i] is None:
			da = ''
		else:
			da = dist_area[i]
		file_name = '{0}{1}{2}_{3}.csv'.format(file_path, dn, da, type)
		ct = 0
		while not os.path.exists(file_name):
			ct += 1
			try:
				informs, _ = get_district_information(district=dist_name[i],
				                                               area=dist_area[i],
				                                               type=type,
				                                               maxpage=100,
				                                               attemp_times=attemp_times,
				                                               verbose=False)
				data = pd.DataFrame(informs)
				data.to_csv(file_name, index=False, encoding='utf_8_sig')
			except Exception as e:
				print(e)
			if ct >= attemp_times:
				break
		print(dist_name[i] + da, '已经提取完毕')


if __name__ == '__main__':
	for k, v in LianJiaMap.items():
		print(k, v)

	url = 'https://su.fang.lianjia.com/loupan/'
	# data = grasp(url, method='requests', is_agent=True)
	# soup = BeautifulSoup(data, 'html.parser')

	# get_district_information(type='ershoufang', area='A1')

	# url1 = 'https://su.lianjia.com/ershoufang/107100591525.html'
	# url2 = 'https://su.lianjia.com/chengjiao/107100695259.html'
	# res1 = get_info_in_per_url(url1, 'ershoufang')
	# res2 = get_info_in_per_url(url2, 'chengjiao')

	# url3 = 'https://su.lianjia.com/ershoufang/'
	# data = grasp(url3, method='requests', is_agent=True)
	# soup = BeautifulSoup(data, 'html.parser')
	#
	# urlist = soup.select('.resblock-name a')
	# page_url = [pg_url['href'] for pg_url in urlist]

	urls = get_urls_in_per_url(url, 'loupan', True )

	# data = grasp(urls[0], method='requests', is_agent=True)
	# soup = BeautifulSoup(data, 'html.parser')

	# house_info = soup.select('.x-box li')
	# urls = get_urls_in_per_url(url3, 'ershoufang')
	#
	#
	infs = get_info_in_per_url(urls[0], type='loupan', verbose=False)