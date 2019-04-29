#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JiaChengXu'
__mtime__ = '2019/4/27'
"""
import pandas as pd
import pymysql
import tqdm
import numpy as np

def clean_nan_in_float(x):
	try:
		return float(x)
	except:
		return 0

def clean_nan_in_int(x):
	try:
		return int(x)
	except:
		return 0

def clean_nian(x):
	try:
		return int(x.split('年')[0])
	except:
		return 0


def clean_m_square(x):
	return float(x.split('㎡')[0])

def clean_m_square_2(x):
	try:
		return int(str(x).split('㎡')[0])
	except:
		return 0

def clean_baifenhao(x):
	string = x.split('%')[0]
	try:
		return int(string)
	except:
		return 0

def clean_rongjilv(x):
	try:
		x = float(x)
	except:
		x = 0
	return '%.2f' % x

class LianjiaCleanToDB(object):
	def __init__(self, ):
		pass

	def read_data(self, file, form='csv'):
		if form in ['csv', ]:
			self.data = pd.read_csv(file, encoding ='utf-8')

		temp = file.split('/')[-2].split('_')
		self.date = temp[0] + temp[1] + temp[2]
		return self

	def clean_for_db(self, type_):
		if type_ in ['chengjiao', ]:
			self.data = self._clean_chengjiao(self.data)
		elif type_ in ['ershoufang', ]:
			self.data = self._clean_ershoufang(self.data)
		elif type_ in ['zufang', ]:
			self.data = self._clean_zufang(self.data)
		elif type_ in ['loupan', ]:
			self.data = self._clean_loupan(self.data)
		else:
			raise Exception('Unknown type_ %s' % type_)
		return self


	def _clean_chengjiao(self, data):
		cols_name = ['成交总价', '挂牌价格', ]
		for cn in cols_name:
			data[cn] = data[cn].apply(clean_nan_in_float)

		cols_name = ['成交均价', '年代', '成交周期', '调价次数', '带看次数', '关注人数', '浏览次数']
		for cn in cols_name:
			data[cn] = data[cn].apply(clean_nan_in_int)

		data['产权年限'] = data['产权年限'].apply(clean_nian)
		data['面积'] = data['面积'].apply(clean_m_square)
		return data


	def _clean_ershoufang(self, data):
		data['总价'] = data['总价'].apply(clean_nan_in_float)
		data['链家编号'] = data['链家编号'].astype(str)
		data['均价'] = data['均价'].apply(clean_nan_in_int)
		data['产权年限'] = data['产权年限'].apply(clean_nian)
		data['面积'] = data['面积'].apply(clean_m_square)
		return data

	def _clean_zufang(self, data):
		data['租金'] = data['租金'].apply(clean_nan_in_int)
		data['面积'] = data['面积'].apply(clean_m_square_2)
		return data

	def _clean_loupan(self, data):
		data['均价'] = data['均价'].apply(clean_nan_in_int)
		data['绿化率'] = data['绿化率'].apply(clean_baifenhao)
		data['容积率'] = data['容积率'].apply(clean_rongjilv)
		data['产权年限'] = data['产权年限'].apply(clean_nian)
		return data

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
		if type_ in ['chengjiao', ]:
			sql = """CREATE TABLE LIANJIACHENGJIAO_%s (采集时间 CHAR(10), 行政区 CHAR(6), 商圈 CHAR(12), 小区 CHAR(15), 
					 成交均价 INT, 成交日期 CHAR(10), 成交总价 DECIMAL(6, 1), 挂牌价格 DECIMAL(6, 1), 成交周期 CHAR(10), 
					 调价次数 INT, 带看次数 INT, 关注人数 INT, 浏览次数 INT, 户型 CHAR(15), 楼层 CHAR(15), 面积 DECIMAL(4, 1),
					 朝向 CHAR(6), 年代 INT, 装修 CHAR(6), 产权年限 INT, 链家编号 CHAR(15), 交易属性 CHAR(6), 挂牌日期 CHAR(10),
					 房屋用途 CHAR(10), 产权性质 CHAR(10), PRIMARY KEY (链家编号))""" % city.upper()
		elif type_ in ['ershoufang', ]:
			sql = """ CREATE TABLE LIANJIAERSHOUFANG_%s_%s (采集时间 CHAR(10), 行政区 CHAR(6), 商圈 CHAR(12), 小区 CHAR(15), 
			 			      链家编号 CHAR(15), 总价 DECIMAL(6, 1), 均价 INT, 户型 CHAR(15), 楼层 CHAR(15), 面积 DECIMAL(4, 1), 
			 			      朝向 CHAR(6), 装修 CHAR(6), 产权年限 INT, 挂牌日期 CHAR(10), 交易属性 CHAR(6), 上次交易 CHAR(10), 
			 			      房屋用途 CHAR(10), 产权性质 CHAR(10), PRIMARY KEY (链家编号))""" % (city.upper(), self.date)
		elif type_ in ['zufang', ]:
			sql = """CREATE TABLE LIANJIAZUFANG_%s_%s (采集时间 CHAR(10), 行政区 CHAR(6), 商圈 CHAR(12), 小区 CHAR(15), 
                     上架时间 CHAR(10), 房源编号 CHAR(15), 租金 INT, 租赁方式 CHAR(12), 户型 CHAR(15), 面积 INT, 
                     朝向 CHAR(6), PRIMARY KEY (房源编号))""" % (city.upper(), self.date)
		elif type_ in ['loupan', ]:
			sql = """CREATE TABLE LIANJIALOUPAN_%s (采集时间 CHAR(10), 行政区 CHAR(6), 楼盘 CHAR(12), 均价 INT, 
                     开发商 CHAR(50), 绿化率 INT, 容积率 CHAR(8), 物业类型 CHAR(6), 产权年限 INT, 物业公司 CHAR(50), 
                     物业费 CHAR(50))""" % city.upper()
		else:
			raise Exception('Unknown type_ %s' % type_)

		self.execute_sql_command(sql)

	def insert_data(self, city, type_):
		data, cursor = self.data, self.db.cursor()
		columns_name = [f for f in data.columns]

		if type_ in ['chengjiao', ]:
			float_idx = [6, 7, 15]
			suffix = city.upper()
		elif type_ in ['ershoufang', ]:
			float_idx = [5, 9]
			suffix = city.upper() + '_' + self.date
		elif type_ in ['zufang', ]:
			float_idx = []
			suffix = city.upper() + '_' + self.date
		elif type_ in ['loupan', ]:
			float_idx = []
			suffix = city.upper()
		else:
			raise Exception('Unknown type_ %s' % type_)

		clname = ''
		for i in columns_name:
			clname += i + ','

		orginal_sql = "INSERT IGNORE INTO LIANJIA%s_%s (%s) VALUES" % (type_.upper(), suffix, clname[:-1])

		pbar = tqdm.tqdm(total=data.shape[0], desc='WriteSQL')
		for ii in range(data.shape[0]):
			data_sql = ""
			for i, j in enumerate(data.iloc[ii, :]):
				if i in float_idx:
					tmp = str(np.round(j, 1))
				else:
					tmp = str(j)
				data_sql += "'%s'," % tmp

			sql = orginal_sql + '(%s);' % data_sql[:-1]

			try:
				pbar.update(1)
				# 执行sql语句
				cursor.execute(sql)
				# 提交到数据库执行
				self.db.commit()
			except:
				# 如果发生错误则回滚
				self.db.rollback()
		pbar.close()
		cursor.close()

# type_ = 'ershoufang'
type_ = 'zufang'

ljdb = LianjiaCleanToDB()
ljdb.read_data('F:/[7] Source Data/ChinaHouse/2019_04_29/lianjia_information_su_%s.csv' % type_)
ljdb.clean_for_db(type_)
ljdb.connect_db()
ljdb.creat_table('suzhou', type_)
ljdb.insert_data('suzhou', type_)
ljdb.disconnect_db()




