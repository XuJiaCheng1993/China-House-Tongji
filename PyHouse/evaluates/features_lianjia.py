#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JiaChengXu'
__mtime__ = '2019/5/2'
"""

from .get_features import *
from ..cleaner import clean_lianjia_data

class GetLianjiaFeature(BaseEstimator, TransformerMixin):
	def fit(self, X, y=None):
		data = c