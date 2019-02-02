#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JiaChengXu'
__mtime__ = '2019/2/1'
"""

import os
import pandas as pd
from LianJiaSpider import LianJiaMap, str_regular
import datetime
import numpy as np

def time_regular(string):
	try:
		try:
			dt =  datetime.datetime.strptime(string, "%Y-%m-%d")
		except:
			dt = datetime.datetime.strptime(string, "%Y/%m/%d")
	except:
		dt = string
	return dt

def area_regular(string):
	area = string.split('㎡')[0]
	try:
		return float(area)
	except:
		return area

def year_regular(string):
	year = string.split('年')[0]
	try:
		return int(year)
	except:
		return year

def district_csv_merge(file_path, Type, city_name = 'suzhou'):
	file_name = '{0}{1}_{2}.csv'.format(file_path, city_name, Type)
	if not os.path.exists(file_name):
		file_list =  os.listdir(file_path)
		city = pd.DataFrame()
		for dist_name, dist_alias in LianJiaMap.items():
			dist_csv = [f for f in file_list if f.find(Type) >= 0 and f.find(dist_alias) >= 0]
			for dcsv in dist_csv:
				datatmp = pd.read_csv(file_path + dcsv)
				datatmp['所属区'] = dist_name
				city = pd.concat([city, datatmp], axis=0)
		city.to_csv(file_name, index=False, encoding='utf_8_sig')
	else:
		city = pd.read_csv(file_name)
	return city

Type = 'ershoufang'
file_path = './data/'

# def _clean_ershoufang(file_path, Type, city_name = 'suzhou'):
# file_name = '{0}{1}_{2}.csv'.format(file_path, city_name, Type)
# if not os.path.exists(file_name):
file_list =  os.listdir(file_path)
for dist_name, dist_alias in LianJiaMap.items():
	if dist_alias is None:
		continue
	dist_csv = [f for f in file_list if f.find(Type) >= 0 and f.find(dist_alias) >= 0]
	# for dcsv in dist_csv:
	# 	datatmp = pd.read_csv(file_path + dcsv)
	# 	datatmp['所属区'] = dist_name

datatmp = pd.read_csv(file_path + dist_csv[0])
columns = [f for f in datatmp.columns if f not in ['均价', '总价', '链家编号']]
for ic in columns:
	datatmp[ic] =  datatmp[ic].apply(str_regular)

for ic in ['上次交易', '挂牌时间']:
	datatmp[ic] = datatmp[ic].apply(time_regular)

for ic in ['套内面积', '建筑面积']:
	datatmp[ic] = datatmp[ic].apply(area_regular)

datatmp['产权年限'] = datatmp['产权年限'].apply(year_regular)


# usage = ['普通住宅', '商住两用']
#
# Type = 'chengjiao'
# file_path = './data/'
# citydata = district_csv_merge(file_path, Type)
# citydata = citydata[citydata['房屋用途'].isin(usage)].reset_index(drop=True)
#
# date_info = np.zeros([citydata.shape[0], 3], dtype=int)
# for i, date in enumerate(citydata['成交日期'].values):
# 	try:
# 		dt = datetime.datetime.strptime(date, "%Y-%m-%d")
# 	except:
# 		dt =datetime.datetime.strptime(date, "%Y/%m/%d")
# 	date_info[i, :] = [dt.year, dt.month, int(dt.day/10)]
#
# date_info[date_info[:, 2] == 3, 2] = 2
#
#
#
# price = citydata['均价'].values
# ave_price = np.zeros([180])
# amont = np.zeros([180])
# ct = 0
# for year in range(2015, 2020):
# 	for month in range(1, 13):
# 		for week in range(3):
# 			index = np.where(np.sum(date_info == [year, month, week], axis=1) == 3)[0]
# 			if len(index)==0:
# 				tmp = 0
# 			else:
# 				tmp = np.mean(price[index])
# 			ave_price[ct] = tmp
# 			amont[ct] = len(index)
# 			ct += 1
#
# import matplotlib.pyplot as plt
# plt.figure()
# plt.plot(ave_price)
# plt.bar(range(180), amont)
# plt.show()