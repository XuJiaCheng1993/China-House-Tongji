#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JiaChengXu'
__mtime__ = '2019/5/2'
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .utils import *

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'KaiTi,Times New Roman'

gap_map=dict(full=1, half=2, third=3)
gap_name_cn = dict(full='', half='半', third='1/3')

def time_serie_curve(prices, areas, dates, year, gap='full', titles='None'):
	''' 绘制变化曲线
	'''
	## 计算月度 数据
	nums = 12 * len(year) * gap_map[gap]
	avgs = np.zeros([nums, 3])
	for j, (day_beg, day_end) in enumerate(generate_date(year, gap=gap)):
		index = np.logical_and((dates - day_beg).dt.days >= 0, (day_end - dates).dt.days >= 0)
		tmp_price, tmp_area = prices[index], areas[index]
		amount = len(tmp_price)
		if amount > 0:
			avgs[j, 0] = np.sum(tmp_price) / amount
			avgs[j, 1] = np.sum(tmp_area)
			avgs[j, 2] = amount

	## 实际数据数
	used_nums = nums
	for i in reversed(range(nums)):
		if np.any(avgs[i, :] != 0):
			used_nums = i
			break

	## 房价环比增长的月份索引
	index = np.hstack((-1, np.diff(avgs[:, 0]))) > 0

	## 画图
	fig = plt.figure(figsize=(16, 4))
	ax1 = fig.add_subplot(111)

	## 房价
	ax1.bar([f for f in range(nums) if index[f]], avgs[index, 0], color='r') ## 房价环比增长的月份
	ax1.bar([f for f in range(nums) if not index[f]], avgs[~index, 0], color='g') ## 房价环比减少的月份
	ax1.set_xticks([f + (gap_map[gap] - 1) / 2 for f in range(0, nums, 3 * gap_map[gap])])
	ax1.set_xticklabels('%s-%s' % (y, m + 1) for y in year for m in range(0, 12, 3))
	ax1.set_xlim(-0.5 * gap_map[gap], used_nums + 0.5 * gap_map[gap])
	ax1.set_ylim(0, 1.5 * np.max(avgs[:, 0]))
	ax1.set_ylabel('成交均价 / 元')
	ax1.legend(['成交均价',], loc='upper left')

	## 成交量
	ax2 = ax1.twinx()
	ax2.plot(avgs[:used_nums+1, 2], '-s', color='MidnightBlue', linewidth=2)
	ax2.set_ylabel('成交套数 / 套')
	ax2.legend(['成交套数', ], loc='upper right')
	plt.title('%s月度房价成交曲线' % (titles + gap_name_cn[gap]))

def listing_price_change(dataframe_left, dataframe_right, date_left, date_right, merge_on='链家编号', regions=None, city='苏州'):
	data = pd.merge(left=dataframe_left, right=dataframe_right, on=merge_on,
	                suffixes=('_%s' % date_left, '_%s' % date_right))
	name_left, name_right = '均价_%s' % date_left, '均价_%s' % date_right

	data['涨跌'] = (data[name_right].astype(int) - data[name_left].astype(int)).apply(np.sign)
	data['涨跌幅'] = (data[name_right].astype(int) - data[name_left].astype(int)) / data[name_left].astype(int)

	if regions is None:
		regions = ['昆山', '吴江', '姑苏', '工业园区', '高新']
	num_region = len(regions)

	counts, values = [], []
	for rg in regions:
		temp = data[data['行政区'] == rg].reset_index(drop=True)
		counts.append([np.count_nonzero(temp['涨跌'] == f) for f in [-1, 0, 1]])
		values.append([np.mean(temp['涨跌幅'][temp['涨跌'] == f]) for f in [-1, 1]])
	counts, values = np.array(counts), np.array(values)

	plt.figure(figsize=(16, 6))
	for i in range(num_region):
		plt.subplot(2, num_region, i + 1)
		plt.pie(counts[i, :], explode=[0.025, ] * 3, labels=['跌', '横盘', '涨'], autopct='%1.1f%%',
		        colors=['g', 'LightSkyBlue', 'r'])
		if i % num_region == int(num_region/2):
			plt.title('%s各行政区房价挂牌价格变化：%s——%s\n涨跌数量占比' %(city, date_left, date_right))

	plt.subplot(212)
	plt.bar(range(num_region), values[:, 0], width=0.3, color='g')
	plt.bar([f + 0.3 for f in range(5)], values[:, 1], width=0.3, color='r')
	plt.xticks([f + 0.3 for f in range(5)], regions)
	for i in range(num_region):
		plt.text(i, 1.4 * values[i, 0], '-%0.1f%%' % (100 * -values[i, 0]))
		plt.text(i + 0.3, 1.1 * values[i, 1], '%0.1f%%' % (100 * values[i, 1]))
	plt.ylim([1.5 * np.min(values), 1.5 * np.max(values)])
	plt.ylabel('幅度')
	plt.legend(['跌幅', '涨幅'])
	plt.title('涨跌幅度')

