#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/6 11:05
# @Author  : Fred Yang
# @File    : send_mail.py
# @Role    : API发送邮件

import os
import json
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MailAPI():
    def __init__(self, mail_host, mail_port, mail_user, mail_passwd, mail_ssl):
        """
        :param mail_host:   SMTP主机
        :param mail_port:   SMTP端口
        :param mail_user:   SMTP账号
        :param mail_passwd: SMTP密码
        :param mail_ssl:    SSL=True, 如果SMTP端口是465，通常需要启用SSL，  如果SMTP端口是587，通常需要启用TLS
        """
        self.mail_host = mail_host
        self.mail_port = mail_port
        self.__mail_user = mail_user
        self.__mail_passwd = mail_passwd
        self.mail_ssl = mail_ssl

    def send_mail(self, to_list, subject, content, subtype='plain', att='none'):
        """
        :param to_list:  收件人，多收件人半角逗号分割， 必填
        :param subject:  标题， 必填
        :param content:  内容， 必填
        :param subtype:  格式，默认：plain, 可选html
        :param att:      附件，支持单附件，选填
        """
        msg = MIMEMultipart()
        msg['Subject'] = subject  ## 标题
        msg['From'] = self.__mail_user  ## 发件人
        msg['To'] = to_list  # 收件人，必须是一个字符串

        # 邮件正文内容
        msg.attach(MIMEText(content, subtype, 'utf-8'))

        if att != 'None':
            if not os.path.isfile(att):
                raise FileNotFoundError('{0} file does not exist'.format(att))

            dirname, filename = os.path.split(att)
            # 构造附件1，传送当前目录下的 test.txt 文件
            att1 = MIMEText(open(att, 'rb').read(), 'base64', 'utf-8')
            att1["Content-Type"] = 'application/octet-stream'
            # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
            att1["Content-Disposition"] = 'attachment; filename="{0}"'.format(filename)
            msg.attach(att1)

        try:
            if self.mail_ssl == 'true':
                '''SSL加密方式，通信过程加密，邮件数据安全, 使用端口465'''
                print('Use SSL SendMail')
                server = smtplib.SMTP_SSL()
                server.connect(self.mail_host, self.mail_port)  # 连接服务器
                server.login(self.__mail_user, self.__mail_passwd)  # 登录操作
                server.sendmail(self.__mail_user, to_list.split(','), msg.as_string())
                server.close()
            else:
                print('Use TLS SendMail')
                '''使用普通模式'''
                server = smtplib.SMTP()
                server.connect(self.mail_host)  # 连接服务器
                server.login(self.__mail_user, self.__mail_passwd)  # 登录操作
                server.sendmail(self.__mail_user, to_list.split(','), msg.as_string())
                server.close()
                return True
        except Exception as e:
            print(str(e))
            return False


def get_email_info():
    api = 'http://172.16.0.101:9000/app_settings'
    resp = requests.get(api)
    if resp:
        data = json.loads(resp.text)['data']
        return data
