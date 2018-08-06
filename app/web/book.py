#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/5/28 13:53
"""

from flask import request, render_template
from flask_login import current_user

from app.common.httpcode import OK
from app.common.response import SuccessResponse
from app.forms.book import BookForm
from app.models.gift import Gift
from app.models.wish import Wish
from app.spiders.yushu_book import YuShuBook
from app.view.book import BookViewModel
from app.view.trade import TradeInfo
from app.web import api_v1
from utils.common import is_isbn_or_key


@api_v1.route('/book/search', methods=['GET'])
def search():
    form = BookForm(request.args)

    if form.validate():
        keyword = form.keyword.data
        page = form.page.data
        yushu_book = YuShuBook()

        if is_isbn_or_key(keyword):
            yushu_book.search_by_keyword(keyword, page)
        else:
            yushu_book.search_by_isbn(keyword)
        return SuccessResponse(OK, data=yushu_book.books).make()


@api_v1.route('/book/<isbn>/detail')
def book_detail(isbn):
    has_in_gifts = False
    has_in_wishes = False

    # 取书籍详情数据
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)

    if current_user.is_authenticated:
        if Gift.query.filter_by(user_id=current_user.id, isbn=isbn, launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(user_id=current_user.id, isbn=isbn, launched=False).first():
            has_in_wishes = True

    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()

    trade_gifts_model = TradeInfo(trade_gifts)
    trade_wishes_model = TradeInfo(trade_wishes)
    return render_template('book_detail.html', book=book, wishes=trade_wishes_model, gifts=trade_gifts_model,
                           has_in_gifts=has_in_gifts, has_in_wishes=has_in_wishes)
