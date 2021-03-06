#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/6/26 13:43
"""

from sqlalchemy import Column, Integer, String, Text

from ext.db import db


class Book(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 标题
    title = Column(String(50))
    # 作者
    author = Column(String(30), default='未名', server_default='未名')
    # 精装 平装
    binding = Column(String(20))
    # 出版社
    publisher = Column(String(50))
    # 页数
    pages = Column(String(20))
    # 价格
    price = Column(String(20))
    # 出版日期
    pubdate = Column(String(20))
    # isbn码 唯一
    isbn = Column(String(15), nullable=False, unique=True)
    # 简介
    summary = Column(Text(1000))
    # 图片
    image = Column(String(50))
