#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/7/2 16:01
"""

from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash

from app.models.base import Base


class User(Base):
    __table_args = {'mysql_charset': 'utf8mb4'}
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 昵称
    nickname = Column(String(24), nullable=False)
    # 电话号码
    phone_number = Column(String(18), unique=True)
    # 邮箱
    email = Column(String(50), unique=True, nullable=False)
    _password = Column('password', String(64), nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)