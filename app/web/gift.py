from flask import flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from app.models import db
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
def redraw_from_gifts(gid):
    pass
