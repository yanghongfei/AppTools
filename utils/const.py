#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/7 17:42
# @Author  : Fred Yang
# @File    : const.py
# @Role    : 常量信息


import json
import time
import requests
from functools import lru_cache

now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

# import tornado.httpclient
# http_client = tornado.httpclient.HTTPClient()
#
# try:
#     response = http_client.fetch('http://172.16.0.101:9000/app_settings')
#     # print(response.body.decode('utf-8'))
#     data = json.loads(response.body.decode('utf-8'))['data']
# except tornado.httpclient.HTTPError as e:
#     print(e)
# http_client.close()


@lru_cache(maxsize=10)
def load_config():
    api = 'http://172.16.0.101:9000/app_settings'
    try:
        resp = requests.get(api, timeout=5)
    except Exception as e:
        print(e)
        return {}
    # 获取配信信息, 前端传过来
    data = json.loads(resp.text)['data']
    return data


data = load_config()

# Mail配置信息
EMAIL_HOST = data.get('EMAIL_HOST')
EMAIL_PORT = data.get('EMAIL_PORT')
EMAIL_HOST_USER = data.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = data.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = data.get('EMAIL_USE_SSL')

# AliYun SMS信息注意：不要更改
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"

# 用户密钥需要对SMS有权限
ACCESS_KEY_ID = data.get('SMS_ACCESS_KEY_ID')
ACCESS_KEY_SECRET = data.get('SMS_ACCESS_KEY_SECRET')

# 阿里大鱼短信服务设置
sign_name = data.get('SMS_SIGN_NAME')  # 签名
template_code = data.get('SMS_TEMPLATE_CODE')  # 模板ID

# 钉钉配置信息
WebHook = data.get('WEBHOOK')

# 微信配置信息
api_url = 'https://pushbear.ftqq.com/sub'
send_key = data.get('WECHAT_KEY')
