#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JiaChengXu'
__mtime__ = '2019/4/29'
"""

import pandas as pd
import numpy as np
from dateutil.parser import parse

data = pd.read_csv('F:/[7] Source Data/ChinaHouse/2019_03_18/lianjia_information_su_chengjiao.csv')


begin_date = parse('2017-01-01')
data =  data[(pd.to_datetime(data['成交日期']) - begin_date).dt.days >= 0]


## 清洗 '成交总价', '挂牌价格' 中的 '缺失值'
def clean_nan_in_float(x):
	try:
		return float(x)
	except:
		return 0

cols_name = ['成交总价', '挂牌价格', ]
for cn in cols_name:
	data[cn] = data[cn].apply(clean_nan_in_float)

## 清洗 '成交周期', '调价次数', '带看次数', '关注人数', '浏览次数' 中的 '缺失值'
def clean_nan_in_int(x):
	try:
		return int(x)
	except:
		return 0

cols_name = ['成交均价', '年代', '成交周期', '调价次数', '带看次数', '关注人数', '浏览次数' ]
for cn in cols_name:
	data[cn] = data[cn].apply(clean_nan_in_int)

def clean_nian(x):
	return int(x.split('年')[0])

data['产权年限'] = data['产权年限'].apply(clean_nian)

def clean_area(x):
	return float(x.split('㎡')[0])

data['面积'] = data['面积'].apply(clean_area)

# data['行政区'] = data['行政区'].map({k: v for v, k in enumerate(np.unique(data['行政区']))})
#
# data['商圈'] = data['商圈'].map({k: v for v, k in enumerate(np.unique(data['商圈']))})
#
# data['朝向'] = data['朝向'].map({k: v for v, k in enumerate(np.unique(data['朝向']))})
#
# data['装修'] = data['装修'].map({k: v for v, k in enumerate(np.unique(data['装修']))})
#
# data['交易属性'] = data['交易属性'].map({k: v for v, k in enumerate(np.unique(data['交易属性']))})
#
# data['房屋用途'] = data['房屋用途'].map({k: v for v, k in enumerate(np.unique(data['房屋用途']))})
#
# data['产权性质'] = data['产权性质'].map({k: v for v, k in enumerate(np.unique(data['产权性质']))})

def map_louceng(string):
	if '高' in string:
		return 3
	elif '中' in string:
		return 2
	elif '低' in string:
		return 1
	else:
		return 0

def map_louceng_digital(x):
	s = ''
	for i in filter(str.isdigit, x):
		s += i
	try:
		return int(s)
	except:
		return 0

def map_huxing(x):
	s = [int(i) for i in filter(str.isdigit, x)]
	if len(s) == 4:
		return np.array(s).dot(np.array([0.3, 0.45, 0.15, 0.1]))
	else:
		return 0



# data['楼层1'] = data['楼层'].apply(map_louceng)
# data['楼层2'] = data['楼层'].apply(map_louceng_digital)
# data['户型'] = data['户型'].apply(map_huxing)


data['成交日期'] = (pd.to_datetime(data['成交日期']) - begin_date).dt.days / 365

features = [f for f in data.columns if f not in ['采集时间', '小区', '楼层', '成交总价', '成交均价', '成交总价',
                                                 '链家编号', '挂牌日期', '挂牌价格', '面积','调价次数', '带看次数', '关注人数',
                                                 '浏览次数', '成交日期']]


from PyHouse.evaluates.get_features import CategoryTransformer

ct = CategoryTransformer()
data[['行政区', '商圈']] = ct.fit_transform(data[['行政区', '商圈']] )


# dealdate = data['成交日期'].values
#
# X = data[features].values
# y = data['成交总价'].values
#
#
#
#
# from sklearn.model_selection import KFold
# import lightgbm as lgb
# from sklearn.metrics import r2_score
#
# X_tr, X_te = X[dealdate<2, :].copy(), X[dealdate>=2, :].copy()
# y_tr, y_te = y[dealdate<2].copy(), y[dealdate>=2].copy()
#
#
# params = {
#     'learning_rate': 0.005,
#     'boosting_type': 'gbdt',
#     'objective': 'regression',
#     'metric': 'rmse',
#     'sub_feature': 0.8,
#     'num_leaves': 255,
#     'subsample_freq':5,
#     'subsample':0.8,
#     'min_hessian': 1,
#     'lambda_l1':5,
#     'lambda_l2':2.5,
#     'verbose': -1,
# }
#
# def feval(y_pred, lgbdataset):
# 	score = 1-r2_score(lgbdataset.get_label(), y_pred)
# 	return ('1 - r2', score, False)
#
#
# kf = KFold(n_splits=4, shuffle=True, random_state=233).split(X_tr)
# y_val, y_pred, imps = np.zeros_like(y_tr), np.zeros_like(y_te), np.zeros([len(features)])
# for j, (train_index, test_index) in enumerate(kf):
# 	lgb_train = lgb.Dataset(X_tr[train_index, :], y_tr[train_index], free_raw_data=False)
# 	lgb_valid = lgb.Dataset(X_tr[test_index, :], y_tr[test_index], free_raw_data=False)
# 	gbm = lgb.train(params,
# 	                lgb_train,
# 	                num_boost_round=3000,
# 	                valid_sets=lgb_valid,
# 	                verbose_eval=100,
# 	                feval=feval,
# 	                early_stopping_rounds=100)
# 	imps += gbm.feature_importance()
# 	y_val[test_index] = gbm.predict(X_tr[test_index, :])
# 	y_pred += gbm.predict(X_te)
# 	del gbm
#
# y_pred /= 4
# imps /= 4
#
# import matplotlib.pyplot as plt
# plt.rcParams['font.family'] = 'sans-serif'
# plt.rcParams['font.sans-serif'] = 'KaiTi,Times New Roman'
#
# # plt.rc('font', family=['KaiTi', 'Times New Roman'])
# dealdate_1 = dealdate[dealdate<2]
# dealdate_2 = dealdate[dealdate>=2]
#
# plt.figure()
# plt.subplot(311)
# plt.plot(y_tr[np.argsort(dealdate_1)], linewidth=2)
# plt.plot(y_val[np.argsort(dealdate_1)])
# plt.ylabel('成交总价 / 万元')
# plt.xticks([])
# plt.title('苏州房价预测（数据来源某知名房产门户网站）\n 训练集，2017，2018年成交数据：r2=%.2f'%(r2_score(y_tr, y_val)))
# plt.legend(['真实房价', '预测房价'])
# plt.subplot(312)
# plt.plot(y_te[np.argsort(dealdate_2)])
# plt.plot(y_pred[np.argsort(dealdate_2)])
# plt.ylabel('成交总价 / 万元')
# plt.title('测试集，2019成交数据：r2=%.2f' % (r2_score(y_te, y_pred)))
# plt.legend(['真实房价', '预测房价'])
# plt.xticks([])
# plt.subplot(313)
# plt.bar(range(len(features)), imps/np.max(imps))
# features[2] = '挂牌时长'
# plt.xticks(range(len(features)), features)
# plt.yticks([0, 0.25, 0.5, 0.75, 1.0], ['0', '25', '50', '75', '100'])
# plt.ylabel('重要百分比 / %')
# plt.title('各特征重要程度')
# plt.show()

