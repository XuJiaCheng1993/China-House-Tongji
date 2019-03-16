#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JiaChengXu'
__mtime__ = '2019/3/13'
"""
import logging
import os

class Logger(object):
	def __init__(self, filepath='./', filename=''):
		filepath += 'logging/'
		filename += '.txt'
		if not os.path.exists(filepath):
			os.makedirs(filepath)

		logger = logging.getLogger(__name__)
		logger.setLevel(level = logging.INFO)
		handler = logging.FileHandler(filepath + filename)
		handler.setLevel(logging.INFO)
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		handler.setFormatter(formatter)
		logger.addHandler(handler)
		self.logger = logger

	def get_logger(self):
		return self.logger