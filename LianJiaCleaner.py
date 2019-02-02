#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JiaChengXu'
__mtime__ = '2019/2/1'
"""

import os
import pandas as pd
from LianJiaSpider import LianJiaMap
import datetime
import numpy as np

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



usage = ['普通住宅', '商住两用']

Type = 'chengjiao'
file_path = './data/'
citydata = district_csv_merge(file_path, Type)
citydata = citydata[citydata['房屋用途'].isin(usage)].reset_index(drop=True)

date_info = np.zeros([citydata.shape[0], 3], dtype=int)
for i, date in enumerate(citydata['成交日期'].values):
	try:
		dt = datetime.datetime.strptime(date, "%Y-%m-%d")
	except:
		dt =datetime.datetime.strptime(date, "%Y/%m/%d")
	date_info[i, :] = [dt.year, dt.month, int(dt.day/10)]

date_info[date_info[:, 2] == 3, 2] = 2



price = citydata['均价'].values
ave_price = np.zeros([180])
amont = np.zeros([180])
ct = 0
for year in range(2015, 2020):
	for month in range(1, 13):
		for week in range(3):
			index = np.where(np.sum(date_info == [year, month, week], axis=1) == 3)[0]
			if len(index)==0:
				tmp = 0
			else:
				tmp = np.mean(price[index])
			ave_price[ct] = tmp
			amont[ct] = len(index)
			ct += 1

import matplotlib.pyplot as plt
plt.figure()
plt.plot(ave_price)
plt.bar(range(180), amont)
plt.show()