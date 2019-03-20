#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JiaChengXu'
__mtime__ = '2019/3/19'
"""
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from .Config import UserAgents
import random

phantomjs_driver_path = r'D:\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\bin\phantomjs.exe',

def get_url(url):
	dcap = dict(DesiredCapabilities.PHANTOMJS)
	#从USER_AGENTS列表中随机选一个浏览器头，伪装浏览器
	dcap["phantomjs.page.settings.userAgent"] = (random.choice(UserAgents))
	# 不载入图片，爬页面速度会快很多
	dcap["phantomjs.page.settings.loadImages"] = False
	# 设置代理
	# service_args = ['--proxy=127.0.0.1:9999','--proxy-type=socks5']
	#打开带配置信息的phantomJS浏览器
	driver = webdriver.PhantomJS(executable_path=phantomjs_driver_path, desired_capabilities=dcap)
	# 隐式等待5秒，可以自己调节
	driver.implicitly_wait(5)
	# 设置10秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项
	# 以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。
	driver.set_page_load_timeout(10)
	# 设置10秒脚本超时时间
	# driver.set_script_timeout(10)

	html = driver.get(url)
	return html