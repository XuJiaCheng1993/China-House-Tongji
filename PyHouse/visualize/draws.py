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

## 基础字体设置
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'KaiTi, Times New Roman'
plt.rcParams['axes.unicode_minus']=False


gap_map=dict(full=1, half=2, third=3)
gap_name_cn = dict(full='', half='半', third='1/3')

def time_serie_curve(prices, areas, dates, year, gap='full', titles='None'):
	''' 绘制房价随时间变化曲线
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

def price_change_plot(dataframe_left, dataframe_right, date_left, date_right, merge_on='链家编号',
                         key_word='行政区',regions=None, city='苏州'):
	''' 绘制挂牌价格变化情况
	'''
	## 根据链家编号定位相同房源
	data = pd.merge(left=dataframe_left, right=dataframe_right, on=merge_on,
	                suffixes=('_%s' % date_left, '_%s' % date_right))
	name_left, name_right = '均价_%s' % date_left, '均价_%s' % date_right

	## 计算涨跌及涨跌幅
	data['涨跌'] = (data[name_right].astype(int) - data[name_left].astype(int)).apply(np.sign)
	data['涨跌幅'] = (data[name_right].astype(int) - data[name_left].astype(int)) / data[name_left].astype(int)

	## 需要分析的行政区 或者 商圈
	if regions is None:
		regions = ['昆山', '吴江', '姑苏', '工业园区', '高新']
	num_region = len(regions)

	## 统计涨跌数量 和 幅度
	counts, values = [], []
	for rg in regions:
		temp = data[data[key_word].str.contains(rg)].reset_index(drop=True)
		counts.append([np.count_nonzero(temp['涨跌'] == f) for f in [-1, 0, 1]])
		values.append([np.mean(temp['涨跌幅'][temp['涨跌'] == f]) for f in [-1, 1]])
	counts, values = np.array(counts), np.array(values)

	## 画图
	plt.figure(figsize=(16, 6))
	## 每个区域的涨跌数量
	for i in range(num_region):
		plt.subplot(2, num_region, i + 1)
		plt.pie(counts[i, :], explode=[0.025, ] * 3, labels=['跌', '横盘', '涨'], autopct='%1.1f%%',
		        colors=['g', 'LightSkyBlue', 'r'])
		if i % num_region == int(num_region/2):
			plt.title('%s各%s房价挂牌价格变化：%s——%s\n涨跌数量占比' %(city, key_word, date_left, date_right))
		plt.xlabel('%s:共%d套' % (regions[i], sum(counts[i, :])))

	## 每个区域的涨跌幅度
	plt.subplot(212)
	plt.bar(range(num_region), values[:, 0], width=0.3, color='g')
	plt.bar([f + 0.3 for f in range(num_region)], values[:, 1], width=0.3, color='r')
	plt.xticks([f + 0.3 for f in range(num_region)], regions)
	for i in range(num_region):
		plt.text(i, 1.4 * values[i, 0], '-%0.1f%%' % (100 * -values[i, 0]))
		plt.text(i + 0.3, 1.1 * values[i, 1], '%0.1f%%' % (100 * values[i, 1]))
	plt.ylim([1.5 * np.min(values), 1.5 * np.max(values)])
	plt.ylabel('幅度')
	plt.legend(['跌幅', '涨幅'])
	plt.title('涨跌幅度')


def rent_price_plot(data_esf, data_zf, city='苏州', date='--'):
	''' 绘制各商圈 挂牌价格 与 租金情况
	'''
	## 统计 商圈数
	areas = np.unique(data_esf['行政区'] + '-' + data_esf['商圈'])
	shangquan = [f.split('-')[-1] for f in areas]
	xingzhengqu = [f.split('-')[0] for f in areas]
	xingzhengqu_nums = np.array([np.count_nonzero(np.array(xingzhengqu) == f) for f in np.unique(xingzhengqu)])
	xingzhengqu_nums = np.cumsum(np.hstack((0, xingzhengqu_nums)))

	## 计算每个商圈的挂牌均价和租金均价
	avgPrice = np.zeros([len(areas)])
	avgZujin = np.zeros_like(avgPrice)
	for i, sqn in enumerate(areas):
		avgPrice[i] = np.mean(data_esf[data_esf['商圈'] == sqn.split('-')[-1]]['均价'].astype(int).values)
		temp = data_zf['租金'].astype(int) / data_zf['面积'].astype(int)
		avgZujin[i] = np.mean(temp[data_zf['商圈'] == sqn.split('-')[-1]].values)
	avgZujin[np.isnan(avgZujin)] = 0

	## 画图
	fig = plt.figure(figsize=(16, 6))
	## 绘制挂牌均价
	ax1 = fig.add_axes([0.05, 0.55, 0.9, 0.4])
	for i in range(len(xingzhengqu_nums) - 1):
		ax1.bar(range(xingzhengqu_nums[i], xingzhengqu_nums[i + 1]),
		        avgPrice[xingzhengqu_nums[i]:xingzhengqu_nums[i + 1]])
	ax1.legend(np.unique(xingzhengqu))
	ax1.plot(avgPrice, color='PaleVioletRed')
	ax1.set_xticks(range(len(areas)))
	ax1.set_xticklabels(shangquan, fontdict=dict(rotation='vertical', verticalalignment='top'))
	ax1.set_xlim(-1, len(areas))
	ax1.set_ylabel('挂牌均价 元/平方米')
	ax1.set_title('%s%s各商圈挂牌均价及租金' % (date, city))

	## 绘制租金
	ax2 = fig.add_axes([0.05, 0.05, 0.9, 0.3])
	for i in range(len(xingzhengqu_nums) - 1):
		ax2.bar(range(xingzhengqu_nums[i], xingzhengqu_nums[i + 1]),
		        avgZujin[xingzhengqu_nums[i]:xingzhengqu_nums[i + 1]])
	ax2.set_xlim(-1, len(areas))
	ax2.invert_yaxis()
	ax2.set_xticks([])
	ax2.set_ylabel('租金 元/平方米')
	ax2.plot(avgZujin, color='PaleVioletRed')