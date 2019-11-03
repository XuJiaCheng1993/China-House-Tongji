#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JiaChengXu'
__mtime__ = '2019/3/18'
"""

import json
from itertools import product

area_esf_1 = ['gaoxin1', 'xiangcheng', 'wujiang', 'kunshan']
condi_esf_1 = [None, ]
area_esf_2 = ['gongyeyuan', 'gusu', 'wuzhong']
condi_esf_2 = ['a1a2a3', 'a4a5', 'a6a7']
args_esf = [f for f in product(area_esf_1, condi_esf_1)] +  [f for f in product(area_esf_2, condi_esf_2)]

area_cj_1 = ['gaoxin1', 'xiangcheng', 'wujiang', 'kunshan', 'wuzhong']
condi_cj_1 = [None, ]
area_cj_2 = ['gongyeyuan',]
condi_cj_2 = ['a1a2a4', 'a3', 'a5a6a7']
area_cj_3 = ['gusu', ]
condi_cj_3 = ['a1a2', 'a3a4a5a6a7']
args_cj = [f for f in product(area_cj_1, condi_cj_1)] +  [f for f in product(area_cj_2, condi_cj_2)] \
          + [f for f in product(area_cj_3, condi_cj_3)]

area_cj_nj = ['gulou', 'jianye', 'qinhuai', 'xuanwu', 'yuhuatai', 'qixia',
              'jiangning', 'pukou']
condi_cj_nj = [['p1p2p7p8', 'p3', 'p4', 'p5', 'p6'],
              ['p1p2p3', 'p4p5', 'p6p7p8'],
              ['p1p2p6', 'p3', 'p4', 'p5p7p8']	,
		      ['p1p2p3p4', 'p5p6p7p8'],
		      [None, ],
		      [None, ],
		      ['p1p2p3', 'p4p6p7p8', 'p5'],
		      ['p1p2p3p4', 'p5p6p7p8']]

args_cj_nj = []
[[args_cj_nj.append(f) for f in product([area_cj_nj[i], ], condi_cj_nj[i])] for i in range(7)]

filtepath = 'G:\\WebData\\ChinaHouse\\'
configs = {'DataSavePath':filtepath,
           'SuzhouLiaJia':{'CJ':args_cj,
		                   'ESF':args_esf,
		                   'ZF':args_esf + [('changshu', None), ],
		                   'XF':[(None, None), ]},
           'NanjingLiaJia':{'CJ':args_cj_nj,
                            },
           'ShangHaiLiaJia':{},
           'Suzhou5i5j':{'CJ':[(None, None), ],
                         'ESF':[(None, None), ],
                         'ZF':[(None, None), ],
                         'XF':[(None, None), ]},
           'Nanjing5i5j':{'CJ':[(None, None), ],
                         'ESF':[(None, None), ],
                         'ZF':[(None, None), ],
                         'XF':[(None, None), ]},
           'ShangHai5i5j':{'CJ':[(None, None), ],
                         'ESF':[(None, None), ],
                         'ZF':[(None, None), ],
                         'XF':[(None, None), ]},
		  }


with open('./MyConfig.txt', 'w') as file_obj:
    json.dump(configs, file_obj)
