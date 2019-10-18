"""
@File : drift.py
@Author: Zyeoh
@Desc :
@Date : 2019/10/18
"""
from app.libs.enums import PendingStatus


class DriftCollection:
    def __init__(self, drifts, current_user_id):
        self.data = []
        self.__parse(drifts, current_user_id)

    def __parse(self, drifts, current_user_id):
        for drift in drifts:
            temp = DriftViewModel(drift, current_user_id)
            self.data.append(temp.data)


class DriftViewModel:
    def __init__(self, drift, current_user_id):
        self.data = {}
        self.data = self.__parse(drift, current_user_id)

    # 是赠送者还是索要者,不建议使用直接current_user,高耦合
    # 没有用到类变量和实例变量，静态方法
    @staticmethod
    def requester_or_gifter(drift, current_user_id):
        if drift.requester_id == current_user_id:
            you_are = 'requester'
        else:
            you_are = 'gifter'
        return you_are

    def __parse(self, drift, current_user_id):
        # 构建一个字典，需在页面显示的字段信息，从原始模型中读出赋值
        you_are = self.requester_or_gifter(drift, current_user_id)
        # 通过枚举类下的方法获得交易的状态
        pending_status = PendingStatus.pending_str(drift.pending, you_are)
        r = {
            'you_are': you_are,
            'drift_id': drift.id,
            'book_title': drift.book_title,
            'book_author': drift.book_author,
            'book_img': drift.book_img,
            'date': drift.create_datetime.strftime('%Y-%m-%d'),
            'operator': drift.requester_nickname if you_are != 'requester' else drift.gifter_nickname,
            'message': drift.message,
            'address': drift.address,
            # 状态信息
            'status_str': pending_status,
            'recipient_name': drift.recipient_name,
            'mobile': drift.mobile,
            'status': drift.pending,

        }
        return r
