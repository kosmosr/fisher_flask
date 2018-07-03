#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/7/3 13:54
"""
from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime

from app.models.base import Base


class Wish(Base):
    __table_args = {'mysql_charset': 'utf8mb4'}
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    create_time = Column(DateTime, default=datetime.now())
