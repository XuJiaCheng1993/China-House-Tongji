#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JiaChengXu'
__mtime__ = '2019/4/27'
"""

import tqdm
import numpy as np
from ..cleaner import clean_lianjia_data
from .db_bases import BaseDB


class LianjiaDB(BaseDB):
	def __init__(self, *args, **kwargs):
		super(LianjiaDB, self).__init__(*args, **kwargs)

	def clean_for_db(self, type_):
		if type_ in ['chengjiao', ]:
			kinds = 2
		elif type_ in ['ershoufang', ]:
			kinds = 0
		elif type_ in ['zufang', ]:
			kinds = 3
		elif type_ in ['loupan', ]:
			kinds = 1
		else:
			raise Exception('Unknown type_ %s' % type_)

		self.data = clean_lianjia_data(self.data, kinds)
		return self

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
                     物业费 DECIMAL(4, 2))""" % city.upper()
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
