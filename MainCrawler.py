#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JiaChengXu'
__mtime__ = '2019/1/31'
"""

from LianJiaSpider import LianjiaTotal
chengjiao_dict = dict(dist_name = ['昆山', '高新', '吴中', '相城', '吴江', '工业园区',
                                   '工业园区', '工业园区', '工业园区', '姑苏', '姑苏', '姑苏'],
					  dist_area = [None, None, None, None, None, 'A1A2', 'A3', 'A4',
					               'A5A6A7', 'A1A2', 'A3A4', 'A5A6A7'],
					  type = 'chengjiao',
					  file_path = './data/')

ershoufang_dict = dict(dist_name = ['昆山', '高新', '相城', '吴江', '吴中', '工业园区',
                                   '工业园区', '工业园区', '姑苏', '姑苏', '姑苏'],
					   dist_area = [None, None, None, None, 'A1A2A3A4', 'A5A6A7', 'A1A2A3', 'A4A5',
					               'A6A7', 'A1A2', 'A3A4', 'A5A6A7'],
					   type = 'ershoufang',
					   file_path = './data/')

LianjiaTotal(**chengjiao_dict)
LianjiaTotal(**ershoufang_dict)