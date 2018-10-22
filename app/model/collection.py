from app.ext import db,orm


class Collection(db.Model):
    __tablename__ = 'collection'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(32), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # sql orm框架在映射创建User对象的时候并不会执行init初始化方法
    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'name']

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

    # repr()方法显示一个可读字符串
    def __repr__(self):
        return '<collection: %s %s>' % (self.name, self.id)
