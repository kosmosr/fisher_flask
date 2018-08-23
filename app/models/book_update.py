#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/8/9 10:06
图书更新处理表
"""
from sqlalchemy import Column, Integer, String

from app.common.enums import BookUpdateStatus
from ext.db import db


class BookUpdate(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    isbn = Column(String(15), nullable=False)
    status = Column(Integer, default=BookUpdateStatus.UNTREATED.value)
