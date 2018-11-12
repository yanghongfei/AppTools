#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/12 15:03
# @Author  : Fred Yang
# @File    : app_dingtalk.py
# @Role    : Tornado POST DingTalk


import os
import sys
import time
import json
import tornado.web

Base_DIR = os.path.dirname(os.path.dirname(os.path.abspath('__file__')))
sys.path.append(Base_DIR)

from utils import const
from utils.send_dingtalk import DingTalkApi


class DingTalkHandler(tornado.web.RequestHandler):
    """钉钉通知Handler路由"""

    def get(self, *args, **kwargs):
        return self.write('Hello, SendDingTalk, Please use POST SendDingTalk!')

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode('utf-8'))

        msgtype = data.get('msgtype', None)
        content = data.get('content', None)
        title = data.get('title', None)
        url = data.get('url', None)
        phone = data.get('phone', None)
        is_at_all = data.get('is_at_all', None)

        # 返回信息
        resp = {

            'status': 0,
            'data': data,
            'datetime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
            'msg': 'OK'
        }

        if not title and not content and not msgtype:
            resp['status'] = '-2'
            resp['msg'] = '参数不能为空'
            return self.write(resp)

        if phone == 'None':
            phone_list_new = []
        else:
            phone_list_old = phone.split(',')
            phone_list_new = []
            for phone in phone_list_old:
                if len(phone) == 11:
                    phone_list_new.append(phone)
                else:
                    resp['status'] = '-3'
                    resp['msg'] = '电话号码不合法'
                    return self.write(resp)

        obj = DingTalkApi(webhook=const.WebHook)
        r_data = {
            'msgtype': msgtype,
            'title': title,
            'content': content,
            'url': url
        }
        try:
            r = obj.send_messages(data=r_data, at_phone=phone_list_new, is_at_all=is_at_all)
        except Exception as e:
            error = repr(e)
            resp['status'] = '-4'
            resp['msg'] = error
            return self.write(resp)
        else:
            if r['errmsg'] == 'ok':
                return self.write(resp)
