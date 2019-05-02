#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JiaChengXu'
__mtime__ = '2019/5/2'
"""
from .cleaner_pandas_based_method import *

def clean_cj(data):
	''' 清理成交数据
	'''

	## 链家编号必须为字符串，且无重复，存入db中将作为主键
	data['链家编号'] = data['链家编号'].astype(str)
	if  data['链家编号'].nunique() != data.shape[0]:
		data.drop_duplicates(subset='链家编号', inplace=True)

	## 清理 '成交总价', '挂牌价格'  保留到小数点后1位， 缺省值0代替
	for cn in ['成交总价', '挂牌价格', ]:
		data[cn] = data[cn].apply(numerical2string, args=('0.0', '.1f'))

	## 清理 '成交均价', '年代', '成交周期', '调价次数', '带看次数', '关注人数', '浏览次数'  保留到整数型，缺省值0代替
	for cn in ['成交均价', '年代', '成交周期', '调价次数', '带看次数', '关注人数', '浏览次数']:
		data[cn] = data[cn].apply(numerical2string, args=('0', 'd'))

	## 清理 '产权年限', 年中的字符'年'， 并以整数型保留，缺省值0代替
	data['产权年限'] = data['产权年限'].apply(remove_string_in_numerical, args=('0', '年', 0, 'd'))

	## 清理 '面积', 年中的字符'㎡'， 保留到小数点后1位， 缺省值0代替
	data['面积'] = data['面积'].apply(remove_string_in_numerical, args=('0.0', '㎡', 0, '.1f'))
	return data

def clean_esf(data):
	''' 清理而二手房数据
	'''
	## 链家编号必须为字符串，且无重复，存入db中将作为主键
	data['链家编号'] = data['链家编号'].astype(str)
	if  data['链家编号'].nunique() != data.shape[0]:
		data.drop_duplicates(subset='链家编号', inplace=True)

	## 清理 '总价', '均价'  分别保留到小数点后1位 和 整数型， 缺省值0代替
	data['总价'] = data['总价'].apply(numerical2string, args=('0.0', '.1f'))
	data['均价'] = data['均价'].apply(numerical2string, args=('0', 'd'))

	## 清理 '产权年限', 年中的字符'年'， 并以整数型保留，缺省值0代替
	data['产权年限'] = data['产权年限'].apply(remove_string_in_numerical, args=('0', '年', 0, 'd'))

	## 清理 '面积', 年中的字符'㎡'， 保留到小数点后1位， 缺省值0代替
	data['面积'] = data['面积'].apply(remove_string_in_numerical, args=('0.0', '㎡', 0, '.1f'))
	return data

def clean_zf(data):
	''' 清理而租房数据
	'''
	## 房源编号必须为字符串，且无重复，存入db中将作为主键
	data['房源编号'] = data['房源编号'].astype(str)
	if  data['房源编号'].nunique() != data.shape[0]:
		data.drop_duplicates(subset='房源编号', inplace=True)

	## 清理 '租金'  保留到整数型，缺省值0代替
	data['租金'] = data['租金'].apply(numerical2string, args=('0', 'd'))

	## 清理 '面积', 年中的字符'㎡'， 保留到整数型， 缺省值0代替
	data['面积'] = data['面积'].apply(remove_string_in_numerical, args=('0', '㎡', 0, 'd'))
	return data

def clean_lp(data):
	''' 清理楼盘/新房数据
	'''
	## 清理 '均价'  保留到整数型，缺省值0代替
	data['均价'] = data['均价'].apply(numerical2string, args=('0', 'd'))

	## 清理 '绿化率', 中的字符'%'， 并以整数型保， 缺省值0代替
	data['绿化率'] = data['绿化率'].apply(remove_string_in_numerical, args=('0', '%', 0, 'd'))

	## 清理 '容积率',  保留到小数点后2位， 缺省值0代替
	data['容积率'] = data['容积率'].apply(remove_string_in_numerical, args=('0.00', ' ', 0, '.2f'))

	## 清理 '产权年限', 年中的字符'年'， 并以整数型保留，缺省值0代替
	data['产权年限'] = data['产权年限'].apply(remove_string_in_numerical, args=('0', '年', 0, 'd'))

	## 清理 '容积率',  保留到小数点后2位， 缺省值0代替
	data['物业费'] = data['物业费'].apply(remove_string_in_numerical, args=('0', '元', 0, '.2f'))
	return data

__function_list = [clean_esf, clean_lp, clean_cj, clean_zf]

def clean_lianjia_data(data, types=0):
	return __function_list[types](data)




