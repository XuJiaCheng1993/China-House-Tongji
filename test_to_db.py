#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JiaChengXu'
__mtime__ = '2019/5/2'
"""

from PyHouse.todb import LianjiaDB

# data_lp = pd.read_csv('F:/[7] Source Data/ChinaHouse/2019_03_19/lianjia_information_su_loupan.csv')

db = LianjiaDB()
db.read_data('F:/[7] Source Data/ChinaHouse/2019_03_19/lianjia_information_su_loupan.csv')
db.clean_for_db(type_='loupan')
db.connect_db()
db.creat_table('suzhou', 'loupan')
db.insert_data('suzhou', 'loupan')
db.disconnect_db()
