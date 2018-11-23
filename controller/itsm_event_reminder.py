#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/23 9:57
# @Author  : Fred Yang
# @File    : itsm_event_reminder.py
# @Role    : ITSM模块事件提醒


import json
import tornado.web
from database import db_session
from models import EventReminder
from utils.const import now_time


class EventHandler(tornado.web.RequestHandler):
    """事件路由 增删改查"""

    def get(self, *args, **kwargs):
        event_info = db_session.query(EventReminder).all()
        title = 'penDevOps事件提醒'
        self.render('event_reminder.html', title=title, event_info=event_info)

    def post(self, *args, **kwargs):
        '''新增一条事件'''
        data = json.loads(self.request.body.decode("utf-8"))

        name = data.get('name', None)
        content = data.get('content', None)
        email = data.get('email', None)
        advance_at = data.get('advance_at', None)
        expire_at = data.get('expire_at', None)

        if not name and not content and not email and not advance_at and not expire_at:
            resp = {
                'status': -1,
                'data': data,
                'datetime': now_time,
                'msg': '参数不能为空'
            }
            return self.write(resp)

        try:
            name_info = db_session.query(EventReminder).filter(EventReminder.name == name).first()
            if name_info:
                resp = {
                    'status': -2,
                    'data': data,
                    'datetime': now_time,
                    'msg': 'Name: {} 已经存在'.format(name)
                }
                return self.write(resp)
            else:
                db_session.add(
                    EventReminder(name=name, content=content, email=email, advance_at=advance_at, expire_at=expire_at))
                db_session.commit()
                resp = {
                    'status': 0,
                    'data': data,
                    'datetime': now_time,
                    'msg': '添加成功'
                }
                return self.write(resp)
        except Exception as e:
            print(e)
            db_session.rollback()

    def put(self, *args, **kwargs):
        '''更新信息'''
        data = json.loads(self.request.body.decode("utf-8"))
        name = data.get('name', None)
        content = data.get('content', None)
        email = data.get('email', None)
        advance_at = data.get('advance_at', None)
        expire_at = data.get('expire_at', None)

        try:
            event_info = {
                "content": content,
                "email": email,
                "advance_at": advance_at,
                "expire_at": expire_at,
            }
            db_session.query(EventReminder).filter(EventReminder.name == name).update(event_info)
            db_session.commit()
            resp = {
                'status': 0,
                'data': data,
                'datetime': now_time,
                'msg': '更新成功'
            }
            return self.write(resp)
        except Exception as e:
            print(e)
            db_session.rollback()

    def delete(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        name = data.get('name', None)
        try:
            db_session.query(EventReminder).filter(EventReminder.name == name).delete(synchronize_session=False)
            db_session.commit()
            resp = {
                'status': 0,
                'data': data,
                'datetime': now_time,
                'msg': '删除成功'
            }
            return self.write(resp)
        except Exception as e:
            print(e)
            db_session.rollback()
