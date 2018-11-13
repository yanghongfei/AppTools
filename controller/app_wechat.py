#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/13 14:27
# @Author  : Fred Yang
# @File    : app_wechat.py
# @Role    : 微信通知handler


import time
import json
import requests
import tornado.web

from utils import const


class WechatHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        return self.write('Hello, SendWechat, Please use POST SendWechat!')

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode('utf-8'))
        text = data.get('text', None)
        desp = data.get('desp', None)

        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        # 返回信息
        resp = {

            'status': 0,
            'data': data,
            'datetime': now_time,
            'msg': 'OK'
        }

        if not text and not desp:
            resp['status'] = '-2'
            resp['msg'] = '参数不能为空'
            return self.write(resp)
        else:
            desp_data = 'desp:{},\nnow_time:{}'.format(desp, now_time)
            params = {
                'sendkey': const.send_key,
                'text': text,
                'desp': desp_data  # 给内容加一个时间，因为平台五分钟内不能发重复内容
            }

        try:
            requests.get(const.api_url, params=params)
        except Exception as e:
            error = repr(e)
            resp['status'] = '-4'
            resp['msg'] = error
            return self.write(resp)
        else:
            return self.write(resp)
