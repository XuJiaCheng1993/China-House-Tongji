#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JiaChengXu'
__mtime__ = '2019/5/2'
"""

import pandas as pd
import pymysql

class BaseDB(object):
	def __init__(self, date=None):
		self.date = date

	def read_data(self, file, form='csv'):
		if form in ['csv', ]:
			self.data = pd.read_csv(file, encoding='utf-8')

		if self.date is None:
			temp = file.split('/')[-2].split('_')
			self.date = temp[0] + temp[1] + temp[2]
		return self

	def clean_for_db(self, type_):
		pass

	def connect_db(self):
		self.db = pymysql.connect("localhost", "root", "root", "chinahouse")

	def disconnect_db(self):
		self.db.close()

	def execute_sql_command(self, sql):
		cursor = self.db.cursor()
		cursor.execute(sql)
		cursor.close()

	def drop_table(self, table_name):
		sql = 'DROP TABLE %s' % table_name
		self.execute_sql_command(sql)

	def creat_table(self, city, type_):
		pass

	def insert_data(self, city, type_):
		pass