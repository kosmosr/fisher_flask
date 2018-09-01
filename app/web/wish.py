from flask import g

from app import db
from app.common.const import REQUEST_USER_ID, SAVE_WISH_ERROR, SATISFY_WISH_ERROR, SATISFY_WISH_MSG, BOOK_ISBN_ERROR, \
    USER_CANNOT_DRIFT, SATISFY_WISHER_ERROR
from app.common.response import ErrorResponse, SuccessResponse
from app.decorator import login_required
from app.models.gift import Gift
from app.models.user import User
from app.models.wish import Wish
from app.spiders.yushu_book import YuShuBook
from app.view.wish import MyWishes
from config import config
from utils.common import is_isbn_or_key
from utils.email import send_email
from . import api_v1


@login_required
@api_v1.route('/wishes', methods=['GET'])
def my_wish():
    uid = getattr(g, REQUEST_USER_ID)
    wishes_of_mine = Wish.get_user_wishes(uid)
    isbns = [wish.isbn for wish in wishes_of_mine]
    gift_counts = Wish.get_gift_counts(isbns)
    wishes = MyWishes(wishes_of_mine, gift_counts)
    return SuccessResponse(data=wishes.gifts)()


@login_required
@api_v1.route('/wishes/<isbn>', methods=['GET'])
def save_to_wish(isbn):
    uid = getattr(g, REQUEST_USER_ID)
    user = User.query.filter_by(id=uid).first()
    if is_isbn_or_key(isbn):
        return ErrorResponse(BOOK_ISBN_ERROR).make()
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    if not yushu_book.first:
        return ErrorResponse(BOOK_ISBN_ERROR).make()
    if user.can_save_to_list(str(isbn)):
        with db.auto_commit():
            wish = Wish()
            wish.isbn = isbn
            wish.user_id = user.id
            db.session.add(wish)
    else:
        return ErrorResponse(SAVE_WISH_ERROR).make()
    return SuccessResponse()()


@login_required
@api_v1.route('/wish/<int:wid>', methods=['GET'])
def satisfy_wish(wid):
    """
    向他人赠送书籍
    :param wid: 心愿id
    :return:
    """
    uid = getattr(g, REQUEST_USER_ID)
    wish = Wish.query.get_or_404(wid)
    wisher = User.query.filter(User.id == wish.user_id, User.is_deleted == False).first_or_404()
    gift = Gift.query.filter_by(user_id=uid, isbn=wish.isbn).first()
    if not gift:
        return ErrorResponse(SATISFY_WISH_ERROR).make()
    current_wish = Wish.query.filter_by(user_id=wisher.id, launched=False, isbn=wish.isbn).first()
    if not current_wish:
        return ErrorResponse(SATISFY_WISHER_ERROR).make()
    can = wisher.can_send_drift()
    if not can:
        return ErrorResponse(USER_CANNOT_DRIFT).make()
    gifter = User.query.filter(User.id == gift.user_id, User.is_deleted == False).first()
    drift_url = config.FRONT_DRIFT_URL
    send_email(wisher.email, '有人想送你一本书', 'email/satisify_wish.html', wisher=wisher, gifter=gifter, gift=gift,
               drift_url=drift_url, wish=wish)
    return SuccessResponse(data=SATISFY_WISH_MSG)()


@login_required
@api_v1.route('/wish/<isbn>', methods=['DELETE'])
def redraw_from_wish(isbn):
    uid = getattr(g, REQUEST_USER_ID)
    wish = Wish.query.filter_by(isbn=isbn, launched=False, user_id=uid).first_or_404()
    with db.auto_commit():
        wish.is_deleted = True
    return SuccessResponse()()
