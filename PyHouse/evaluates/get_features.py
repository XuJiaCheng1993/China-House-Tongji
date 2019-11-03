#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JiaChengXu'
__mtime__ = '2019/5/2'
"""
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class CategoryTransformer(BaseEstimator, TransformerMixin):
	def __init__(self):
		pass

	def fit(self, X, y=None):
		if isinstance(X, pd.DataFrame):
			X = X.values
		uni = []
		for i in range(X.shape[1]):
			uni.append({k:v for v, k in enumerate(np.unique(X[:, i]))})

		self.uniques = uni
		return self

	def transform(self, X):
		X = pd.DataFrame(X)
		for i, cl in enumerate(X.columns):
			X[cl] = X[cl].map(self.uniques[i])
		return X.values

def _get_int_from_string(string):
	for i in filter(str.isdigit, string):
		yield i

def get_huxing_feature(x, weight=None, na=0):
	if weight is None:
		weight = np.array([0.3, 0.45, 0.15, 0.1])
	s = [int(i) for i in _get_int_from_string(x)]
	if len(s) == 4:
		return np.array(s).dot(weight)
	else:
		return na

def get_louceng_feature(x, na=0):
	s = ''
	for i in _get_int_from_string(x):
		s += i
	try:
		return int(s)
	except:
		return na

