from flask import flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from app.const.enums import PendingStatus
from app.models.drift import Drift
from ext.db import db
from app.models.gift import Gift
from app.view.gift import MyGifts
from . import web

__author__ = '七月'


@web.route('/my/gifts')
@login_required
def my_gifts():
    gifts_of_mine = Gift.get_user_gifts(current_user.id)
    isbns = [gift.isbn for gift in gifts_of_mine]
    wish_counts = Gift.get_wish_counts(isbns)
    view = MyGifts(gifts_of_mine, wish_counts)
    return render_template('my_gifts.html', gifts=view.gifts)


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.user_id = current_user.id
            current_user.beans += 0.5
            db.session.add(gift)
    else:
        flash('这本书已添加至你的赠书清单或已存在你的心愿清单，请不要重复添加')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/gifts/<gid>/redraw')
@login_required
def redraw_from_gifts(gid):
    gift = Gift.query.filter_by(id=gid, launched=False).first_or_404()
    drift = Drift.query.filter_by(gift_id=gid, pending=PendingStatus.Waiting.value).first()
    if drift:
        flash('这个礼物正处于交易状态，请先前往鱼漂完成该交易')
    with db.auto_commit():
        current_user.beans -= 0.5
        gift.is_deleted = True
    return redirect(url_for('web.my_gifts'))
