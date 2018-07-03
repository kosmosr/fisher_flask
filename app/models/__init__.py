#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/6/26 13:43
"""
from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy as _SQLAlcheymy


class SQLAlchemy(_SQLAlcheymy):

    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


db = SQLAlchemy()
