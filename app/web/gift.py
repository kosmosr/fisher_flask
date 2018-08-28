from decimal import *

from flask import g

from app.common.const import REQUEST_USER_ID, SAVE_BOOK_ERROR, REDRAW_GIFT_ERROR, BOOK_ISBN_ERROR
from app.common.enums import PendingStatus
from app.common.response import SuccessResponse, ErrorResponse
from app.decorator import login_required
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.user import User
from app.spiders.yushu_book import YuShuBook
from app.view.gift import MyGifts
from ext.db import db
from utils.common import is_isbn_or_key
from . import api_v1

__author__ = '七月'


@login_required
@api_v1.route('/gifts', methods=['GET'])
def my_gifts():
    uid = getattr(g, REQUEST_USER_ID)
    gifts_of_mine = Gift.get_user_gifts(uid)
    isbns = [gift.isbn for gift in gifts_of_mine]
    wish_counts = Gift.get_wish_counts(isbns)
    view = MyGifts(gifts_of_mine, wish_counts)
    return SuccessResponse(data=view.gifts)()


@login_required
@api_v1.route('/gifts/<isbn>', methods=['GET'])
def save_to_gifts(isbn):
    if is_isbn_or_key(isbn):
        return ErrorResponse(BOOK_ISBN_ERROR).make()
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    if not yushu_book.first:
        return ErrorResponse(BOOK_ISBN_ERROR).make()
    uid = getattr(g, REQUEST_USER_ID)
    user = User.query.get(uid)
    if user.can_save_to_list(isbn):
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.user_id = user.id
            user.beans += Decimal(0.5).quantize(Decimal('0.00'))
            db.session.add(gift)
    else:
        return ErrorResponse(SAVE_BOOK_ERROR).make()
    return SuccessResponse()()


@login_required
@api_v1.route('/gifts/<gid>', methods=['DELETE'])
def redraw_from_gifts(gid):
    uid = getattr(g, REQUEST_USER_ID)
    user = User.query.get_or_404(uid)
    gift = Gift.query.filter_by(id=gid, launched=False, user_id=uid).first_or_404()
    drift = Drift.query.filter_by(gift_id=gid, pending=PendingStatus.Waiting.value).first()
    if drift:
        return ErrorResponse(REDRAW_GIFT_ERROR).make()
    with db.auto_commit():
        user.beans -= Decimal(0.5).quantize(Decimal('0.00'))
        gift.is_deleted = True
    return SuccessResponse()()
