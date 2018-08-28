from decimal import Decimal

from flask import request, g
from sqlalchemy import or_, desc

from app.common.const import REQUEST_USER_ID, SEND_DRIFT_IS_YOURSELF, USER_CANNOT_DRIFT
from app.common.enums import PendingStatus
from app.common.response import ErrorResponse, SuccessResponse
from app.decorator import login_required
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.user import User
from app.models.wish import Wish
from app.schema.validate import DriftValSchema, DriftPendingStatusSchema
from app.view.drift import DriftCollection
from ext.db import db
from . import api_v1


@login_required
@api_v1.route('/drift/<int:gid>', methods=['GET'])
def drift(gid):
    uid = getattr(g, REQUEST_USER_ID)
    current_user = User.query.get_or_404(uid)
    current_gift = Gift.query.get_or_404(gid)
    if current_gift.is_yourself_gift(uid):
        # 不能自己给自己发起鱼漂
        return ErrorResponse(SEND_DRIFT_IS_YOURSELF).make()
    # 检验当前用户能否发起鱼漂请求
    can = current_user.can_send_drift()
    if not can:
        return ErrorResponse(USER_CANNOT_DRIFT).make()
    user_from_gift = User.query.get_or_404(current_gift.user_id).summary
    user_from_gift.update({'user_beans': str(current_user.beans)})
    return SuccessResponse(data=user_from_gift)()


@login_required
@api_v1.route('/drifts', methods=['POST'])
def send_drift():
    uid = getattr(g, REQUEST_USER_ID)
    schema = DriftValSchema(strict=True)
    data = schema.load(request.get_json()).data
    current_gift = Gift.query.get_or_404(data['gift_id'])
    user_from_gift = User.query.get_or_404(current_gift.user_id)
    current_user = User.query.get_or_404(uid)
    save_drift(data, current_gift, user_from_gift, current_user)
    # todo 提醒用户 email or sms
    return SuccessResponse()()


@login_required
@api_v1.route('/pending', methods=['GET'])
def pending():
    uid = getattr(g, REQUEST_USER_ID)
    drifts = Drift.query.filter(or_(Drift.requester_id == uid,
                                    Drift.gifter_id == uid)).order_by(desc(Drift.create_time)).all()
    data = DriftCollection(drifts, uid).data
    return SuccessResponse(data=data)()


@login_required
@api_v1.route('/drift/<int:did>', methods=['PATCH'])
def drift_pending(did):
    uid = getattr(g, REQUEST_USER_ID)
    schema = DriftPendingStatusSchema(strict=True)
    status = schema.dump(request.get_json()).data['status']
    with db.auto_commit():
        if status == PendingStatus.Success.value:
            # 邮寄
            drift = Drift.query.filter_by(gifter_id=uid, id=did).first_or_404()
            drift.pending = PendingStatus.Success.value
            gift = Gift.query.filter_by(id=drift.gift_id).first_or_404()
            gift.launched = True
            gift.is_deleted = True

            wish = Wish.query.filter_by(isbn=drift.isbn, user_id=drift.requester_id, launched=False).first_or_404()
            wish.launched = True
            wish.is_deleted = True
        elif status == PendingStatus.Reject.value:
            # 拒绝 当前用户为赠书者
            drift = Drift.query.filter_by(gifter_id=uid, id=did).first_or_404()
            drift.pending = PendingStatus.Reject.value
            drift.is_deleted = True
            requester = User.query.get_or_404(drift.requester_id)
            requester.beans += Decimal(1).quantize(Decimal('0.00'))
        elif status == PendingStatus.Redraw.value:
            # 撤销 当前用户为索要者
            drift = Drift.query.filter_by(id=did, requester_id=uid).first()
            drift.pending = PendingStatus.Redraw.value
            drift.is_deleted = True
            current_user = User.query.get_or_404(uid)
            current_user.beans += Decimal(1).quantize(Decimal('0.00'))
    return SuccessResponse()()


def save_drift(drift_info, current_gift, gifter, current_user):
    """
    保存交易记录
    :param drift:
    :param current_gift: gift实体
    :param gifter: 礼物拥有者
    :param current_user: 当前登录用户
    :return:
    """
    with db.auto_commit():
        drift = Drift()
        drift.recipient_name = drift_info['recipient_name']
        drift.mobile = drift_info['mobile']
        drift.message = drift_info['message']
        drift.address = drift_info['address']

        drift.gift_id = current_gift.id
        drift.requester_id = current_user.id
        drift.requester_nickname = current_user.nickname
        drift.gifter_id = gifter.id
        drift.gifter_nickname = gifter.nickname

        book = current_gift.book
        drift.book_title = book['title']
        drift.book_author = book['author']
        drift.book_img = book['image']
        drift.isbn = book['isbn']
        current_user.beans -= Decimal(1).quantize(Decimal('0.00'))
        db.session.add(drift)
