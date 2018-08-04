#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/8/1 14:47
"""
from sqlalchemy import Column, Integer, String, SmallInteger

from app.const.enums import PendingStatus
from app.models.base import Base


class Drift(Base):
    """
    一次具体的交易信息
    """
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 邮寄信息
    recipient_name = Column(String(20), nullable=False)
    address = Column(String(100), nullable=False)
    message = Column(String(200))
    mobile = Column(String(20), nullable=False)
    # 书籍信息
    isbn = Column(String(15))
    book_title = Column(String(50))
    book_author = Column(String(30))
    book_img = Column(String(50))
    # 请求者信息
    requester_id = Column(Integer)
    requester_nickname = Column(String(20))
    # 赠送者信息
    gift_id = Column(Integer)
    gifter_id = Column(Integer)
    gifter_nickname = Column(String(20))
    # 交易状态 默认等待状态
    pending = Column(SmallInteger, default=PendingStatus.Waiting.value)
