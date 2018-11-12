#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/12 13:39
# @Author  : Fred Yang
# @File    : send_dingtalk.py
# @Role    : DingTalk 钉钉机器人通知


import json
import requests


class DingTalkApi():
    def __init__(self, webhook):
        """
        :param webhook:  DingDing WebHook地址
        WebHook 机器人申请参考:https://open-doc.dingtalk.com/docs/doc.htm?spm=0.0.0.0.0Sds7z&treeId=257&articleId=105733&docType=1
        发送消息官方示例：https://open-doc.dingtalk.com/docs/doc.htm?spm=a219a.7629140.0.0.karFPe&treeId=257&articleId=105735&docType=1
        """
        self.webhook = webhook
        self.headers = {'Content-Type': 'application/json; charset=utf-8'}

    def send_messages(self, data, at_phone, is_at_all=False):
        """
        发送通知消息，支持格式：text, link, markdown
        :param data: 一些标题、内容数据
        :param at_phone: 需要@人的手机号,没有则为：None
        :param is_at_all: 是否需要@全员，@全员为：True
        :return:
        """
        msgtype = data['msgtype']
        content = data['content']
        title = data['title']
        url = data['url']

        if msgtype == 'link':
            '''发送超链接消息'''
            msg_data = {
                "msgtype": 'link',
                "link": {
                    "text": content,
                    "at": {
                        "atMobiles": at_phone,
                        "isAtAll": is_at_all
                    },
                    "title": title,
                    "picUrl": "",
                    "messageUrl": url
                }
            }


        else:
            '''默认发送普通消息'''
            msg_data = {
                "msgtype": "text",
                "text": {
                    "content": content
                },
                "at": {
                    "atMobiles": at_phone,
                    "isAtAll": is_at_all
                }
            }

        r = requests.post(self.webhook, headers=self.headers, data=json.dumps(msg_data))
        resp = json.loads(r.text)
        return resp


if __name__ == '__main__':
    pass
