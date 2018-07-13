from flask import flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from app import db
from app.models.wish import Wish
from app.view.wish import MyWishes
from . import web

__author__ = '七月'


@web.route('/my/wish')
@login_required
def my_wish():
    wishes_of_mine = Wish.get_user_wishes(current_user.id)
    isbns = [wish.isbn for wish in wishes_of_mine]
    gift_counts = Wish.get_gift_counts(isbns)
    wishes = MyWishes(wishes_of_mine, gift_counts)
    return render_template('my_wish.html', wishes=wishes.gifts)


@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            wish = Wish()
            wish.user_id = current_user.id
            wish.isbn = isbn
            db.session.add(wish)
    else:
        flash('这本书已添加至你的赠书清单或已存在你的心愿清单，请不要重复添加')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/satisfy/wish/<int:wid>')
def satisfy_wish(wid):
    pass


@web.route('/wish/book/<isbn>/redraw')
def redraw_from_wish(isbn):
    pass
