#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/7 17:42
# @Author  : Fred Yang
# @File    : const.py
# @Role    : 常量信息

import json
import requests

api = 'http://172.16.0.101:9000/app_settings'
resp = requests.get(api)
# 获取配信信息, 前端传过来
data = json.loads(resp.text)['data']

# Mail配置信息
EMAIL_HOST = data['EMAIL_HOST']
EMAIL_PORT = data['EMAIL_PORT']
EMAIL_HOST_USER = data['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = data['EMAIL_HOST_PASSWORD']
EMAIL_USE_SSL = data['EMAIL_USE_SSL']

# AliYun SMS信息注意：不要更改
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"

# 用户密钥需要对SMS有权限
ACCESS_KEY_ID = data['SMS_ACCESS_KEY_ID']
ACCESS_KEY_SECRET = data['SMS_ACCESS_KEY_SECRET']

# 阿里大鱼短信服务设置
sign_name = data['SMS_SIGN_NAME']  # 签名
template_code = data['SMS_TEMPLATE_CODE']  # 模板ID



#钉钉配置信息
WebHook = data['WEBHOOK']