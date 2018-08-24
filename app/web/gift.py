from decimal import *

from flask import flash, redirect, url_for, render_template, g
from flask_login import current_user

from app.common.const import REQUEST_USER_ID, SAVE_BOOK_ERROR
from app.common.enums import PendingStatus
from app.common.httpcode import OK
from app.common.response import SuccessResponse, ErrorResponse
from app.decorator import login_required
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.user import User
from app.view.gift import MyGifts
from ext.db import db
from . import api_v1

__author__ = '七月'


@api_v1.route('/my/gifts')
def my_gifts():
    gifts_of_mine = Gift.get_user_gifts(current_user.id)
    isbns = [gift.isbn for gift in gifts_of_mine]
    wish_counts = Gift.get_wish_counts(isbns)
    view = MyGifts(gifts_of_mine, wish_counts)
    return render_template('my_gifts.html', gifts=view.gifts)


@login_required
@api_v1.route('/gifts/<isbn>', methods=['GET'])
def save_to_gifts(isbn):
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
    return SuccessResponse(OK).make()


@api_v1.route('/gifts/<gid>/redraw')
def redraw_from_gifts(gid):
    gift = Gift.query.filter_by(id=gid, launched=False).first_or_404()
    drift = Drift.query.filter_by(gift_id=gid, pending=PendingStatus.Waiting.value).first()
    if drift:
        flash('这个礼物正处于交易状态，请先前往鱼漂完成该交易')
    with db.auto_commit():
        current_user.beans -= 0.5
        gift.is_deleted = True
    return redirect(url_for('web.my_gifts'))
