#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/21 17:51
# @Author  : Fred Yang
# @File    : itsm_fault.py
# @Role    : ITSM模块故障管理


import json
import tornado.web
from utils.const import now_time
from database import db_session
from models import Fault as itsm_fault_info


class FaultHandler(tornado.web.RequestHandler):
    """Fault故障管理路由"""

    def get(self, *args, **kwargs):
        title = 'Fault Info V0.1'
        try:
            fault_info = db_session.query(itsm_fault_info).all()
            # for data in fault_info:
            #     print(data.fault_name)
            self.render('fault_info.html', title=title, fault_info=fault_info)
        except Exception as e:
            print(e)
            db_session.rollback()

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        fault_name = data.get('fault_name', None)
        fault_level = data.get('fault_level', None)
        fault_state = data.get('fault_state', None)
        fault_penson = data.get('fault_penson', None)
        processing_penson = data.get('processing_penson', None)
        fault_report = data.get('fault_report', None)
        fault_start_time = data.get('fault_start_time', None)
        fault_end_time = data.get('fault_end_time', None)
        fault_issue = data.get('fault_issue', None)
        fault_summary = data.get('fault_summary', None)

        if not fault_name and not fault_level and not fault_state and not fault_penson and not fault_start_time and not fault_end_time:
            resp = {
                'status': -1,
                'data': data,
                'datetime': now_time,
                'msg': '参数不能为空'
            }
            return self.write(resp)

        else:
            try:
                name_info = db_session.query(itsm_fault_info).filter(itsm_fault_info.fault_name == fault_name).first()
                if name_info:
                    resp = {
                        'status': -2,
                        'data': data,
                        'datetime': now_time,
                        'msg': 'Name: {} 已经存在'.format(fault_name)
                    }
                    return self.write(resp)
                else:
                    db_session.add(
                        itsm_fault_info(fault_name=fault_name, fault_level=fault_level, fault_state=fault_state,
                                        fault_penson=fault_penson, processing_penson=processing_penson,
                                        fault_report=fault_report, fault_start_time=fault_start_time,
                                        fault_end_time=fault_end_time,
                                        fault_issue=fault_issue,
                                        fault_summary=fault_summary))
                    db_session.commit()

                    resp = {
                        'status': 0,
                        'data': data,
                        'datetime': now_time,
                        'msg': 'Name: {} 添加成功'.format(fault_name)
                    }
                    return self.write(resp)

            except Exception as e:
                db_session.rollback()
                error = repr(e)
                resp = {
                    'status': -3,
                    'data': data,
                    'datetime': now_time,
                    'msg': error
                }

                return self.write(resp)

    def put(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        fault_name = data.get('fault_name', None)
        fault_level = data.get('fault_level', None)
        fault_state = data.get('fault_state', None)
        fault_penson = data.get('fault_penson', None)
        processing_penson = data.get('processing_penson', None)
        fault_report = data.get('fault_report', None)
        fault_start_time = data.get('fault_start_time', None)
        fault_end_time = data.get('fault_end_time', None)
        fault_issue = data.get('fault_issue', None)
        fault_summary = data.get('fault_summary', None)

        try:
            update_info = {
                "fault_level": fault_level,
                "fault_state": fault_state,
                "fault_penson": fault_penson,
                "processing_penson": processing_penson,
                "fault_report": fault_report,
                "fault_start_time": fault_start_time,
                "fault_end_time": fault_end_time,
                "fault_issue": fault_issue,
                "fault_summary": fault_summary,
            }
            db_session.query(itsm_fault_info).filter(itsm_fault_info.fault_name == fault_name).update(update_info)
            db_session.commit()
            resp = {
                'status': 0,
                'data': data,
                'datetime': now_time,
                'msg': '更新成功'
            }
            return self.write(resp)

        except Exception as e:
            db_session.rollback()
            error = repr(e)
            resp = {
                'status': -3,
                'data': data,
                'datetime': now_time,
                'msg': error
            }

            return self.write(resp)

    def delete(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        fault_name = data.get('fault_name', None)

        if not fault_name:
            resp = {
                'status': -1,
                'data': data,
                'datetime': now_time,
                'msg': '参数不能为空'
            }
            return self.write(resp)
        else:
            try:
                db_session.query(itsm_fault_info).filter(itsm_fault_info.fault_name == fault_name).delete(
                    synchronize_session=False)
                db_session.commit()
                resp = {
                    'status': 0,
                    'data': data,
                    'datetime': now_time,
                    'msg': '删除成功'
                }
                return self.write(resp)

            except Exception as e:
                db_session.rollback()
                error = repr(e)
                resp = {
                    'status': -3,
                    'data': data,
                    'datetime': now_time,
                    'msg': error
                }

                return self.write(resp)
