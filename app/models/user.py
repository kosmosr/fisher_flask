#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/7/2 16:01
"""
from datetime import datetime
from math import floor

from sqlalchemy import Column, Integer, String, DateTime, Numeric
from werkzeug.security import generate_password_hash, check_password_hash

from app.common.enums import PendingStatus
from app.models.base import Base
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.wish import Wish
from ext.db import db


class User(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 昵称
    nickname = Column(String(24), nullable=False)
    # 电话号码
    phone_number = Column(String(18), unique=True)
    # 邮箱
    email = Column(String(50), unique=True, nullable=False)
    _password = Column('password', String(128), nullable=False)
    # 鱼豆
    beans = Column(Numeric(8, 2), default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))
    update_time = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        """
        检验密码
        :param raw: 用户输入的密码
        :return: True/False
        """

        return check_password_hash(self.password, raw)

    @staticmethod
    def reset_password(uid, password):
        user = User.query.filter_by(id=uid).first_or_404()
        with db.auto_commit():
            user.password = password
            db.session.add(user)

    def can_send_drift(self, isbn=None):
        if self.beans < 1:
            return False
        current_wish = Wish.query.filter_by(user_id=self.id, launched=False, isbn=isbn).first()
        if not current_wish:
            return False
        success_gifts_count = Gift.query \
            .filter_by(user_id=self.id, launched=True).count()
        success_receive_count = Drift.query \
            .filter_by(requester_id=self.id, pending=PendingStatus.Success.value).count()
        return True if floor(success_receive_count / 2) <= floor(success_gifts_count) else False

    def can_save_to_list(self, isbn):
        # 检验isbn 以及是否存在于yushu api中
        # 用户不能是赠书者又是索要者
        # 不能赠书多次相同图书(未送出 launched=False)
        wishing = Wish.query.filter_by(user_id=self.id, isbn=isbn, launched=False).first()
        gifting = Gift.query.filter_by(user_id=self.id, isbn=isbn, launched=False).first()
        if not wishing and not gifting:
            return True
        else:
            return False

    @property
    def summary(self):
        return dict(
            nickname=self.nickname,
            beans=str(self.beans),
            email=self.email,
            send_receive=f'{self.send_counter}/{self.receive_counter}'
        )
