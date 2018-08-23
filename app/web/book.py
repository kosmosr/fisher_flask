#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/5/28 13:53
"""

from flask import request, g

from app.common.const import REQUEST_USER_ID
from app.common.httpcode import OK
from app.common.response import SuccessResponse
from app.models.gift import Gift
from app.models.wish import Wish
from app.schema.model import BookSchema
from app.schema.validate import BookSearchValSchema
from app.schema.view import BookDetailViewSchema, TradeModelSchema
from app.spiders.yushu_book import YuShuBook
from app.view.trade import TradeInfo
from app.web import api_v1
from utils.common import is_isbn_or_key


@api_v1.route('/books/<keyword>', methods=['GET'])
def search(keyword):
    dict = request.args.to_dict()
    dict.update({'keyword': keyword})
    schema = BookSearchValSchema(strict=True).load(dict)
    data = schema.data
    keyword = data['keyword']
    page = data['page']
    per_page = data['per_page']
    # md5_params = md5_n(keyword + str(page) + str(per_page))

    yushu_book = YuShuBook()
    if is_isbn_or_key(keyword):
        yushu_book.search_by_keyword(keyword, page, per_page)
    else:
        yushu_book.search_by_isbn(keyword)
    pagination = {
        'total': yushu_book.total,
        'current_page': page,
        'per_page': per_page
    }
    # data = [data for data in yushu_book.books if data.]
    return SuccessResponse(OK, data=yushu_book.books, pagination=pagination).make()


@api_v1.route('/book/<isbn>', methods=['GET'])
def book_detail(isbn):
    has_in_gifts = False
    has_in_wishes = False

    # 取书籍详情数据
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    # book = BookViewModel(yushu_book.first)

    uid = getattr(g, REQUEST_USER_ID, None)
    if uid:
        if Gift.query.filter_by(user_id=uid, isbn=isbn, launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(user_id=uid, isbn=isbn, launched=False).first():
            has_in_wishes = True

    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()

    trade_gifts_model = TradeInfo(trade_gifts)
    trade_wishes_model = TradeInfo(trade_wishes)

    book_schema = BookSchema()
    book_data = book_schema.dump(yushu_book.first).data  # type: dict
    has = {'has_in_gifts': has_in_gifts, 'has_in_wishes': has_in_wishes}  # type:dict
    trade = TradeModelSchema()
    gifts = {'gifts': trade.dump(trade_gifts_model).data}
    wishes = {'wishes': trade.dump(trade_wishes_model).data}
    schema = BookDetailViewSchema()
    book_data.update(has)
    book_data.update(wishes)
    book_data.update(gifts)
    data = schema.dump(book_data).data
    return SuccessResponse(OK, data=data).make()
