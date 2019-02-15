from app.ext import db, orm
from werkzeug.security import generate_password_hash, check_password_hash
from app.validator.error import ApiException


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account = db.Column(db.String(50))
    secret = db.Column(db.String(500))
    type = db.Column(db.Integer)
    interest = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    _password = db.Column('password', db.String(500))

    collection = db.relationship('Collection', backref='user')

    # sql orm框架在映射创建User对象的时候并不会执行init初始化方法
    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'account', 'secret']

    def keys(self):
        return self.fields

    # 用于隐藏某些key
    def hide(self, *field):
        for key in field:
            self.fields.remove(key)
        return self

    # 用于添加某些key
    def append(self, *field):
        for key in field:
            self.fields.append(key)
        return self

    def __getitem__(self, item):
        return getattr(self, item)

    def __repr__(self):
        return "<User id = %s, mobile = %s>" % (self.id, self.account)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)
        # self._password = "123456"

    # 额外拓展一些业务中需要使用的字段
    @property
    def summary(self):
        return dict(
            nickname=self.account,
            acctounttype=self.type,
        )

    @staticmethod
    def create_user(account, secret):
        user = User()
        user.account = account
        user.password = secret
        db.session.add(user)
        db.session.commit()
        pass

    @staticmethod
    def verify(account, secret):
        user = User.query.filter_by(account=account).first()
        if not user:
            raise ApiException(msg='账号不存在')
        if not user.check_password(secret):
            raise ApiException(msg='密码错误')
        return {'uid': user.id}

    @staticmethod
    def get_user(uid):
        user = User.query.filter_by(id=uid).first()
        if not user:
            raise ApiException(msg='用户不存在')
        else:
            return user

    @staticmethod
    def reset_password(uid, new_password):
        user = User.query.filter_by(id=uid).first()
        if user is None:
            raise ApiException(msg='用户不存在')
        else:
            user.password = new_password
            db.session.commit()

    def check_password(self, raw):
        if not raw:
            return False
        return check_password_hash(self._password, raw)
