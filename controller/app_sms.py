#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/8 10:41
# @Author  : Fred Yang
# @File    : app_sms.py
# @Role    : SendSMS Handler


import json
import tornado.web
from utils import const
from utils.send_sms import SmsApi


class SendSMSHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        return self.write('Hello, SendSMS, Please use POST SendSMS!')

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode('utf-8'))
        msg = data.get('msg', None)
        phone = data.get('phone', None)

        if not msg and not phone:
            resp = {
                'status': -2,
                'msg': '参数不能为空'
            }
            return self.write(resp)

        phone_list = phone.split(',')
        for phone_number in phone_list:
            if len(phone_number) != 11:
                resp = {
                    'status': -1,
                    'msg': '电话号码不合法'
                }
                return self.write(resp)

        obj = SmsApi(const.ACCESS_KEY_ID, const.ACCESS_KEY_SECRET)

        params = {
            "msg": msg
        }

        send_sms = obj.send_sms(phone_numbers=','.join(phone_list), sign_name=const.sign_name,
                                template_code=const.template_code,
                                template_param=params)

        data = json.loads(send_sms.decode('utf-8'))
        r_data = data['Message']
        if r_data == 'OK':
            resp = {
                'status': 0,
                'data': data,
                'msg': '短信发送成功'
            }
            return self.write(resp)
        else:
            resp = {
                'status': -3,
                'data': data,
                'msg': '短信发送失败'
            }
            return self.write(resp)
