#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JiaChengXu'
__mtime__ = '2019/4/27'
"""

import pandas as pd
import numpy as np
from PyHouse.cleaner import clean_lianjia_data
from PyHouse.visualize import time_serie_curve, price_change_plot, rent_price_plot
import matplotlib.pyplot as plt


# data = pd.read_csv('F:/[7] Source Data/ChinaHouse/2019_03_18/lianjia_information_su_chengjiao.csv')

# data_cj = pd.read_csv('F:/[7] Source Data/ChinaHouse/2019_03_18/lianjia_information_su_chengjiao.csv')
#
# column_name = ['链家编号', '均价']
#
# date = ['2019_03_18', '2019_03_28', '2019_04_07', '2019_04_15', '2019_04_22', '2019_04_29']
# data = []
# for dt in date:
# 	temp = pd.read_csv('F:/[7] Source Data/ChinaHouse/%s/lianjia_information_su_ershoufang.csv' % dt)
# 	data.append(clean_lianjia_data(temp, 0))

# data_esf = pd.read_csv('F:/[7] Source Data/ChinaHouse/2019_04_29/lianjia_information_su_ershoufang.csv')
#
# data_zf = pd.read_csv('F:/[7] Source Data/ChinaHouse/2019_04_29/lianjia_information_su_zufang.csv')
# data_lp = pd.read_csv('F:/[7] Source Data/ChinaHouse/2019_03_19/lianjia_information_su_loupan.csv')

#
# data_cj = clean_lianjia_data(data_cj, 2)
#
#
# data_cj = data_cj[data_cj['行政区'] == '工业园区']
#
# price = data_cj['成交均价'].astype(int).values
# area = data_cj['面积'].astype(float).values
#
# time_serie_curve(prices=price, areas=area, dates=pd.to_datetime(data_cj['成交日期']) , year=list(range(2015, 2020)), gap='half', titles='苏州工业园区')
#
# listing_price_change(data[0][['链家编号', '行政区', '商圈', '小区', '均价']], data[-1][column_name], date_left=date[0],
#               date_right=date[-1], key_word='商圈', regions=['湖东', '玲珑', '东环', '狮山', '青剑湖'])


# data_esf = data[0].copy()
# data_esf

date = ['2019_04_07', '2019_04_15', '2019_04_22', '2019_04_29']
data_esf, data_zf = pd.DataFrame(), pd.DataFrame()
for dt in reversed(date):
	tmp_esf = pd.read_csv('F:/[7] Source Data/ChinaHouse/%s/lianjia_information_su_ershoufang.csv' % dt)
	tmp_zf = pd.read_csv('F:/[7] Source Data/ChinaHouse/%s/lianjia_information_su_zufang.csv' % dt)
	data_esf = pd.concat([data_esf, clean_lianjia_data(tmp_esf, 0)], axis=0).reset_index(drop=True)
	data_zf = pd.concat([data_zf, clean_lianjia_data(tmp_zf, 3)], axis=0).reset_index(drop=True)



data_esf.drop_duplicates(subset='链家编号', inplace=True)
data_zf.drop_duplicates(subset='房源编号', inplace=True)

data_esf.sort_values(by='行政区', inplace=True)
data_esf.dropna(inplace=True)

data_zf.sort_values(by='行政区', inplace=True)
data_zf.drop(210, inplace=True)
data_zf.dropna(inplace=True)

# data_esf = clean_lianjia_data(data_esf, 0)
# data_zf = clean_lianjia_data(data_zf, 3)

rent_price_plot(data_esf, data_zf, date='2019-04')

# areas = np.unique(data_esf['行政区'] + '-' + data_esf['商圈'])
#
# avgPrice = np.zeros([len(areas)])
# avgZujin = np.zeros_like(avgPrice)
#
# for i, sqn in enumerate(areas):
# 	avgPrice[i] = np.mean(data_esf[data_esf['商圈']==sqn.split('-')[-1]]['均价'].astype(int).values)
# 	temp = data_zf['租金'].astype(int) / data_zf['面积'].astype(int)
# 	avgZujin[i] = np.mean(temp[data_zf['商圈']==sqn.split('-')[-1]].values)
#
# avgZujin[np.isnan(avgZujin)] = 0
#
#
# shangquan = [f.split('-')[-1] for f in areas]
# xingzhengqu = [f.split('-')[0] for f in areas]
# xingzhengqu_nums = np.array([np.count_nonzero(np.array(xingzhengqu)==f) for f in np.unique(xingzhengqu)])
# xingzhengqu_nums = np.cumsum(np.hstack((0, xingzhengqu_nums)))
#
# fig = plt.figure(figsize=(16, 6))
# ax1 = fig.add_axes([0.05, 0.55, 0.9, 0.4])
# for i in range(len(xingzhengqu_nums) - 1):
# 	ax1.bar(range(xingzhengqu_nums[i], xingzhengqu_nums[i+1]), avgPrice[xingzhengqu_nums[i]:xingzhengqu_nums[i+1]])
# ax1.legend(np.unique(xingzhengqu))
# ax1.plot(avgPrice, color='PaleVioletRed')
# ax1.set_xticks(range(len(areas)))
# ax1.set_xticklabels(shangquan, fontdict=dict(rotation='vertical', verticalalignment='top'))
# ax1.set_xlim(-1, len(areas))
# ax1.set_ylabel('挂牌均价 元/平方米')
# ax1.set_title('苏州各商圈挂牌均价及租金')
#
# ax2 = fig.add_axes([0.05, 0.05, 0.9, 0.3])
# for i in range(len(xingzhengqu_nums) - 1):
# 	ax2.bar(range(xingzhengqu_nums[i], xingzhengqu_nums[i+1]), avgZujin[xingzhengqu_nums[i]:xingzhengqu_nums[i+1]])
# ax2.set_xlim(-1, len(areas))
# ax2.invert_yaxis()
# ax2.set_xticks([])
# ax2.set_ylabel('租金 元/平方米')
# ax2.plot(avgZujin, color='PaleVioletRed')
#
# plt.stackplot()

plt.show()










