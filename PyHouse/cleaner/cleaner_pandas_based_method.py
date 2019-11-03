#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JiaChengXu'
__mtime__ = '2019/5/2'
"""

## To String
def numerical2string(x, na='', fmt='.2f'):
	formats = '%' + fmt
	try:
		return formats % float(x)
	except:
		return na

def remove_string_in_numerical(s, na='', string1='㎡', loc1=0,  fmt='d', string2='~', loc2=0):
	formats = '%' + fmt
	try:
		try:
			return formats % float(str(s).split(string1)[loc1])
		except:
			return formats % float(str(s).split(string1)[loc1].split(string2)[loc2])
	except:
		return na

def statute_unknown_string(s, string=None, na=''):
	if string is None:
		string = ['未知', '无', '暂无数据', '暂无消息', '暂未确定', '待定', '租赁方式未知']

	if s in string:
		return na
	else:
		return s


