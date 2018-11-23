#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/2 17:36
# @Author  : Fred Yang
# @File    : models.py
# @Role    : 数据库信息


from datetime import datetime
from database import Base
from sqlalchemy import Column
from sqlalchemy import String, Integer, DateTime, TIMESTAMP
from sqlalchemy.dialects.mysql import LONGTEXT
from database import init_db


class Fault(Base):
    __tablename__ = 'itsm_fault_info'
    id = Column(Integer, primary_key=True, autoincrement=True)  # ID 自增长
    fault_name = Column(String(100), nullable=False)  # 故障名称
    fault_level = Column(Integer, nullable=False)  # 故障级别,1,2,3,4为故障等级
    fault_state = Column(Integer, nullable=False)  # 故障状态，0:关闭 1：进行中
    fault_penson = Column(String(100), nullable=False)  # 故障责任人
    processing_penson = Column(String(100), nullable=True)  # 故障处理人员
    fault_report = Column(LONGTEXT, nullable=True)  # 故障报告，附件
    fault_start_time = Column(DateTime, nullable=False)  # 故障开始时间
    fault_end_time = Column(DateTime, nullable=False)  # 故障结束时间
    fault_duration = Column(String(100), nullable=True)  # 故障影响时间，分钟
    fault_issue = Column(String(100), nullable=True)  # 故障原因
    fault_summary = Column(String(100), nullable=True)  # 故障总结
    create_at = Column(DateTime, nullable=False, default=datetime.now())  # 记录创建时间
    update_at = Column(TIMESTAMP, nullable=False, default=datetime.now())  # 记录更新时间


class EventReminder(Base):
    __tablename__ = 'itsm_event_reminder'
    id = Column(Integer, primary_key=True, autoincrement=True)  # ID 自增长
    name = Column(String(100), nullable=True)  # 事件名称
    content = Column(String(100), nullable=True)  # 事件的描述
    email = Column(String(100), nullable=True)  # 通知人员email
    advance_at = Column(Integer, nullable=True)  # 提前多少天提醒
    expire_at = Column(DateTime, nullable=True)  # 事件过期时间
    create_at = Column(DateTime, nullable=False, default=datetime.now())  # 记录创建时间
    update_at = Column(TIMESTAMP, nullable=False, default=datetime.now())  # 记录更新时间

#init_db()  #第一次初始化使用
