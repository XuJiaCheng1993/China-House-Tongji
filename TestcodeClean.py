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
from PyHouse.visualize import time_serie_curve, listing_price_change
import matplotlib.pyplot as plt
plt.rcParams['axes.unicode_minus']=False

# data = pd.read_csv('F:/[7] Source Data/ChinaHouse/2019_03_18/lianjia_information_su_chengjiao.csv')

data_cj = pd.read_csv('F:/[7] Source Data/ChinaHouse/2019_03_18/lianjia_information_su_chengjiao.csv')

column_name = ['链家编号', '均价']

date = ['2019_03_18', '2019_03_28', '2019_04_07', '2019_04_15', '2019_04_22', '2019_04_29']
data = []
for dt in date:
	temp = pd.read_csv('F:/[7] Source Data/ChinaHouse/%s/lianjia_information_su_ershoufang.csv' % dt)
	data.append(clean_lianjia_data(temp, 0))

# data_esf = pd.read_csv('F:/[7] Source Data/ChinaHouse/2019_03_18/lianjia_information_su_ershoufang.csv')

# data_zf = pd.read_csv('F:/[7] Source Data/ChinaHouse/2019_03_18/lianjia_information_su_zufang.csv')
# data_lp = pd.read_csv('F:/[7] Source Data/ChinaHouse/2019_03_19/lianjia_information_su_loupan.csv')


data_cj = clean_lianjia_data(data_cj, 2)


data_cj = data_cj[data_cj['行政区'] == '工业园区']

price = data_cj['成交均价'].astype(int).values
area = data_cj['面积'].astype(float).values

time_serie_curve(prices=price, areas=area, dates=pd.to_datetime(data_cj['成交日期']) , year=list(range(2015, 2020)), gap='half', titles='苏州工业园区')

listing_price_change(data[0][['链家编号', '行政区', '商圈', '小区', '均价']], data[-1][column_name], date_left=date[0],
              date_right=date[-1])


# newdata = data[0][['链家编号', '行政区', '商圈', '小区', '均价']]
# for i in range(1, 6):
# 	newdata = pd.merge(left=newdata, right=data[i][column_name], on='链家编号', suffixes=('', '_%s'%date[i]))
#
#
#
# newdata['涨跌'] = (newdata['均价_2019_04_29'].astype(int) - newdata['均价'].astype(int)).apply(np.sign)
# newdata['涨跌幅'] = (newdata['均价_2019_04_29'].astype(int) - newdata['均价'].astype(int)) / newdata['均价'].astype(int)
#
#
#
# counts, values =[], []
# for rg in ['昆山', '吴江', '姑苏', '工业园区', '高新']:
# 	temp = newdata[newdata['行政区']==rg].reset_index(drop=True)
#
# 	counts.append([np.count_nonzero(temp['涨跌'] == f) for f in [-1, 0, 1]])
# 	values.append([np.mean(temp['涨跌幅'][temp['涨跌'] == f]) for f in [-1, 1]])
#
# counts, values = np.array(counts), np.array(values)
#
# plt.figure(figsize=(16, 6))
# for i in range(5):
# 	plt.subplot(2, 5, i + 1)
# 	plt.pie(counts[i, :], explode=[0.02, ]* 3, labels=['跌', '横盘', '涨' ], autopct='%1.1f%%',
# 	        colors=['g','LightSkyBlue','r'])
# plt.subplot(212)
# plt.bar(range(5), values[:, 0], width=0.3, color='g' )
# plt.bar([f + 0.3 for f in range(5)], values[:, 1], width=0.3, color='r' )
# plt.xticks([f + 0.3 for f in range(5)], ['昆山', '吴江', '姑苏', '工业园区', '高新'])
# for i in range(5):
# 	plt.text(i, 1.4 * values[i, 0], '-%0.1f%%' % (100 * -values[i, 0]))
# 	plt.text(i + 0.3, 1.1 * values[i, 1], '%0.1f%%' % (100 * values[i, 1]))
# plt.ylim([1.5 * np.min(values), 1.5 * np.max(values)])
# plt.ylabel('幅度')
# plt.legend(['跌幅', '涨幅'])
#
# np.unique(newdata['行政区'])



plt.show()










