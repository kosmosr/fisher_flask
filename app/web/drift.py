from flask import flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user

from app.forms.book import DriftForm
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.user import User
from app.view.book import BookViewModel
from ext.db import db
from . import web

__author__ = '七月'


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    current_gift = Gift.query.get_or_404(gid)
    if current_gift.is_yourself_gift(current_user.id):
        flash('这本书是你自己的，不能向自己索要书籍噢')
        return redirect(url_for('web.book_detail', isbn=current_gift.isbn))
    can = current_user.can_send_drift()
    if not can:
        return render_template('not_enough_beans.html', beans=current_user.beans)
    user_from_gift = User.query.get_or_404(current_gift.user_id)
    form = DriftForm(request.form)
    if request.method == 'POST' and form.validate():
        save_drift(form, current_gift, user_from_gift)
        # 提醒用户 email or sms
        pass
    return render_template('drift.html', gifter=user_from_gift, user_beans=current_user.beans, form=form)


@web.route('/pending')
def pending():
    pass


@web.route('/drift/<int:did>/reject')
def reject_drift(did):
    pass


@web.route('/drift/<int:did>/redraw')
def redraw_drift(did):
    pass


@web.route('/drift/<int:did>/mailed')
def mailed_drift(did):
    pass


def save_drift(drift_form: DriftForm, current_gift, gifter):
    with db.auto_commit():
        drift = Drift()
        drift_form.populate_obj(drift)

        drift.gift_id = current_gift.id
        drift.requester_id = current_user.id
        drift.requester_nickname = current_user.nickname
        drift.gift_id = gifter.id
        drift.gifter_nickname = gifter.nickname

        book = BookViewModel(current_gift.book.first)
        drift.book_title = book.title
        drift.book_author = book.author
        drift.book_img = book.image
        drift.isbn = book.isbn
        current_user.beans -= 1
        db.session.add(drift)
