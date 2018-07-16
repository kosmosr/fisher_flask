#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/7/2 17:02
"""
from datetime import datetime

from sqlalchemy import Column, Boolean, DateTime

from ext.db import db


class Base(db.Model):
    # 忽略SQLAlchemy对该模型的创表
    # create_time是类变量 程序启动时就会设置默认值 应该在初始化实例时设置时间
    __abstract__ = True
    is_deleted = Column(Boolean, default=False)
    create_time = Column(DateTime)

    def __init__(self):
        self.create_time = datetime.now()

    def set_attrs(self, attrs_dict: dict):
        for k, v in attrs_dict.items():
            if hasattr(self, k) and k != 'id':
                setattr(self, k, v)
