#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JiaChengXu'
__mtime__ = '2019/5/2'
"""

from dateutil.parser import parse

def generate_date(year, gap='full'):
	for y in year:
		days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
		if (y % 4 == 0 and y % 100 != 0) or (y % 100 == 0 and y % 400 == 0):
			days[1] = 29
		for m in range(12):
			if gap == 'half':
				for j in range(2):
					if j == 0:
						yield parse('%s-%s-01' % (y, m + 1)), parse('%s-%s-15' % (y, m + 1))
					else:
						yield parse('%s-%s-16' % (y, m + 1)), parse('%s-%s-%s' % (y, m + 1, days[m]))

			elif gap == 'third':
				for j in range(3):
					if j == 0:
						yield parse('%s-%s-01' % (y, m + 1)), parse('%s-%s-10' % (y, m + 1))
					elif j == 1:
						yield parse('%s-%s-11' % (y, m + 1)), parse('%s-%s-20' % (y, m + 1))
					else:
						yield parse('%s-%s-21' % (y, m + 1)), parse('%s-%s-%s' % (y, m + 1, days[m]))
			else:
				yield parse('%s-%s-01' % (y, m + 1)), parse('%s-%s-%s' % (y, m + 1, days[m]))






