#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/5 17:34
# @Author  : Fred Yang
# @File    : database.py
# @Role    : 连接数据库信息


from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from settings import DB_INFO as MYSQL_CONFIG

engine = create_engine(
    f'mysql+mysqlconnector://{MYSQL_CONFIG["user"]}:{MYSQL_CONFIG["password"]}@{MYSQL_CONFIG["host"]}/{MYSQL_CONFIG["db"]}?charset=utf8')

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    Base.metadata.create_all(engine)
