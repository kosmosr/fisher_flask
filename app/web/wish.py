from flask import redirect, url_for, render_template, g
from flask_login import current_user

from app import db
from app.common.const import REQUEST_USER_ID, SAVE_WISH_ERROR
from app.common.httpcode import OK
from app.common.response import ErrorResponse, SuccessResponse
from app.decorator import login_required
from app.models.user import User
from app.models.wish import Wish
from app.view.wish import MyWishes
from . import api_v1

__author__ = '七月'


@api_v1.route('/my/wish')
def my_wish():
    wishes_of_mine = Wish.get_user_wishes(current_user.id)
    isbns = [wish.isbn for wish in wishes_of_mine]
    gift_counts = Wish.get_gift_counts(isbns)
    wishes = MyWishes(wishes_of_mine, gift_counts)
    return render_template('my_wish.html', wishes=wishes.gifts)


@login_required
@api_v1.route('/wish/<isbn>', methods=['GET'])
def save_to_wish(isbn):
    uid = getattr(g, REQUEST_USER_ID)
    user = User.query.filter_by(id=uid).first()
    if user.can_save_to_list(isbn):
        with db.auto_commit():
            wish = Wish()
            wish.isbn = isbn
            wish.user_id = user.id
            db.session.add(wish)
    else:
        return ErrorResponse(SAVE_WISH_ERROR).make()
    return SuccessResponse(OK).make()


@api_v1.route('/satisfy/wish/<int:wid>')
def satisfy_wish(wid):
    pass


@api_v1.route('/wish/book/<isbn>/redraw')
def redraw_from_wish(isbn):
    wish = Wish.query.filter_by(isbn=isbn, launched=False).first_or_404()
    with db.auto_commit():
        wish.is_deleted = True
    return redirect(url_for('web.my_wish'))
