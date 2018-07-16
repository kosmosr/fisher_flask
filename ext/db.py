#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/7/16 16:37
"""
from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy as _SQLAlcheymy, BaseQuery


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'is_deleted' not in kwargs.keys():
            kwargs['is_deleted'] = False
        return super(Query, self).filter_by(**kwargs)


class SQLAlchemy(_SQLAlcheymy):

    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


db = SQLAlchemy(query_class=Query)
