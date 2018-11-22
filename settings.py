#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/5 9:36
# @Author  : Fred Yanghongfei
# @File    : settings.py
# @Role    : 配置文件


import os.path

DB_INFO = {
    'host': '172.16.0.101',
    'user': 'root',
    'port': 3306,
    'password': 'shinezone2015',
    'db': 'OpenDevOps'
}

settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    xsrf_cookies=False,
    cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    # login_url="/login",
    debug=True,
)
