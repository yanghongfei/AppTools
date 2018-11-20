#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/6 16:47
# @Author  : Fred Yang
# @File    : app_mail.py
# @Role    : mail Handler

import os
import sys
import json
import tornado.web

Base_DIR = os.path.dirname(os.path.dirname(os.path.abspath('__file__')))
sys.path.append(Base_DIR)

from utils import const
from utils.send_mail import MailAPI as SendMailAPI


class SendMailHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        return self.write('Hello, SendMail, Please use POST SendMail!')

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode('utf-8'))
        to_list = data.get('to_list', None)
        subject = data.get('subject', None)
        content = data.get('content', None)
        subtype = data.get('subtype', None)
        att = data.get('att', None)


        if not to_list and not subject and not content:
            resp = {
                'status': -1,
                'msg': '收件人、邮件标题、邮件内容不能为空'
            }
            return self.write(resp)

        try:
            obj = SendMailAPI(mail_host=const.EMAIL_HOST, mail_port=const.EMAIL_PORT, mail_user=const.EMAIL_HOST_USER,
                              mail_passwd=const.EMAIL_HOST_PASSWORD,
                              mail_ssl=const.EMAIL_USE_SSL)

            obj.send_mail(to_list, subject, content, subtype=subtype, att=att)
            resp = {
                'status': 0,
                'data': data,
                'msg': '发送成功'
            }
            return self.write(resp)

        except Exception as e:
            print(e)
