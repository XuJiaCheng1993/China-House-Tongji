#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JiaChengXu'
__mtime__ = '2019/10/10'
"""

import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.ticker as ticker
from nirlysis.drawing import set_cn_font
from IPython.display import HTML


file_path =  'G:\WebData\ChinaHouse'
file = os.listdir(file_path)
csv = 'lianjia_information_su_ershoufang.csv'


def agg_function(df):
	return df.values[-1]

def agg_function_price(df):
	if len(df) < 10:
		return 0
	else:
		return np.mean(df)


def get_dt(data):
	price = data.groupby(by='小区').agg({'均价': agg_function_price, '行政区': agg_function, '商圈': agg_function})
	price.sort_values(by='均价', ascending=False, inplace=True)

	d1 = pd.concat([price[price['行政区'] == '工业园区'].iloc[:5, :],
	                price[price['行政区'] == '高新'].iloc[:5, :],
	                price[price['行政区'] == '姑苏'].iloc[:5, :],
	                ])
	d1.sort_values(by='均价', ascending=True, inplace=True)
	d1['pos'] = d1['行政区'] + '-' + d1['商圈']
	return d1

data, dates = pd.DataFrame(), []
for ii in file:
	if csv in os.listdir(os.path.join(file_path, ii)):
		tmp = pd.read_csv(os.path.join(file_path, ii, csv))
		tmp = get_dt(tmp)
		tp = ii.replace('_', '-')
		dates.append(tp)
		tmp['date'] = tp
		data = pd.concat([data, tmp])



colors = dict(zip(['工业园区', '高新', '姑苏',],
                  ['#adb0ff', '#ffb3ff', '#90d595']))




def draw_barchart(date):
	ax.clear()
	set_cn_font()
	dt = data[data['date']==date].copy()
	ax.barh(dt.index, dt['均价'], color=[colors[f] for f in dt['行政区']])
	for i, (value, pos) in enumerate(zip(dt['均价'], dt['pos'])):
		ax.text(value, i, dt.index[i], ha='right', color='#444444', size=14)
		ax.text(value, i - .4, pos, ha='right', va='bottom')
		ax.text(value, i - .1, f'{value:,.0f}',size=14 , ha='left')
	ax.text(1, 0.2, date, transform=ax.transAxes, size=40, ha='right')
	ax.text(0, 1.06, '均价(元)', transform=ax.transAxes, size=12, color='#777777', ha='left')
	ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
	ax.xaxis.set_ticks_position('top')
	ax.tick_params(axis='x', colors='#777777', labelsize=12)
	ax.set_yticks([])
	ax.set_xlim(20000, 95000)
	ax.margins(0, 0.01)
	ax.grid(which='major', axis='x', linestyle='-')
	ax.set_axisbelow(True)
	ax.text(0, 1.10, '苏州高新/姑苏/工业园区各Top5小区房价(2019.03.18-2019.10.07)', va='bottom',
	        transform=ax.transAxes, size=24, weight=600, ha='left')
	ax.text(1, 0, 'by @XuJiaCheng', transform=ax.transAxes, ha='right',
	        color='#777777', bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))
	plt.box(False)



with plt.xkcd():
	fig, ax = plt.subplots(figsize=(15, 8))
	animator = animation.FuncAnimation(fig, draw_barchart, frames=dates)
	# draw_barchart('2019-10-07')
# HTML(animator.to_jshtml())
animator.save('./test.gif', fps=1)
