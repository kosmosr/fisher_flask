from flask import flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import or_, desc

from app.const.enums import PendingStatus
from app.forms.book import DriftForm
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.user import User
from app.models.wish import Wish
from app.view.book import BookViewModel
from app.view.drift import DriftCollection
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
        return redirect(url_for('web.pending'))
    return render_template('drift.html', gifter=user_from_gift.summary, user_beans=current_user.beans, form=form)


@web.route('/pending')
@login_required
def pending():
    drifts = Drift.query.filter(or_(Drift.requester_id == current_user.id,
                                    Drift.gifter_id == current_user.id)).order_by(desc(Drift.create_time)).all()
    views = DriftCollection(drifts, current_user.id)
    return render_template('pending.html', drifts=views.data)


@web.route('/drift/<int:did>/reject')
@login_required
def reject_drift(did):
    """
    拒绝
    :param did:
    :return:
    """
    with db.auto_commit():
        drift = Drift.query.filter(Gift.user_id == current_user.id, Drift.id == did).first_or_404()
        drift.pending = PendingStatus.Reject.value
        requester = User.query.get_or_404(drift.requester_id)
        requester.beans += 1
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/redraw')
@login_required
def redraw_drift(did):
    """
    撤销
    :param did:
    :return:
    """
    with db.auto_commit():
        drift = Drift.query.filter_by(id=did, requester_id=current_user.id).first()
        drift.pending = PendingStatus.Redraw.value
        current_user.beans += 1
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/mailed')
@login_required
def mailed_drift(did):
    """
    邮寄
    :param did:
    :return:
    """
    with db.auto_commit():
        drift = Drift.query.filter_by(gifter_id=current_user.id, id=did).first_or_404()
        drift.pending = PendingStatus.Success.value
        current_user.beans += 1

        gift = Gift.query.filter_by(id=drift.gifter_id).first_or_404()
        gift.launched = True

        wish = Wish.query.filter_by(isbn=drift.isbn, user_id=drift.requester_id, launched=False).first_or_404()
        wish.launched = True
    return redirect(url_for('web.pending'))


def save_drift(drift_form: DriftForm, current_gift, gifter):
    with db.auto_commit():
        drift = Drift()
        drift_form.populate_obj(drift)

        drift.gift_id = current_gift.id
        drift.requester_id = current_user.id
        drift.requester_nickname = current_user.nickname
        drift.gifter_id = gifter.id
        drift.gifter_nickname = gifter.nickname

        book = BookViewModel(current_gift.book)
        drift.book_title = book.title
        drift.book_author = book.author
        drift.book_img = book.image
        drift.isbn = book.isbn
        current_user.beans -= 1
        db.session.add(drift)
