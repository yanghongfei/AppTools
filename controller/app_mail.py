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

from utils.send_mail import get_email_info
from utils.send_mail import MailAPI as SendMailAPI


class SendMailHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        return self.write('Hello, SendMail')

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode('utf-8'))
        to_list = data.get('to_list', None)
        subject = data.get('subject', None)
        content = data.get('content', None)
        subtype = data.get('subtype', None)
        att = data.get('att', None)

        if not to_list and not subject and not content:
            resp = {
                'status': 0,
                'msg': '收件人、邮件标题、邮件内容不能为空'
            }
            return self.write(resp)
        EMAIL_INFO = get_email_info()
        '''获取AppSettings里面登陆信息，实例化SendMailAPI'''
        mail_host = EMAIL_INFO['EMAIL_HOST']
        mail_port = EMAIL_INFO['EMAIL_PORT']
        mail_user = EMAIL_INFO['EMAIL_HOST_USER']
        mail_passwd = EMAIL_INFO['EMAIL_HOST_PASSWORD']
        mail_ssl = EMAIL_INFO['EMAIL_USE_SSL']

        try:
            obj = SendMailAPI(mail_host=mail_host, mail_port=mail_port, mail_user=mail_user, mail_passwd=mail_passwd,
                              mail_ssl=mail_ssl)

            obj.send_mail(to_list, subject, content, subtype=subtype, att=att)
            resp = {
                'status': 0,
                'data': data,
                'msg': '发送成功'
            }
            return self.write(resp)

        except Exception as e:
            print(e)
