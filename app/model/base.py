from app.ext import db,orm


class BaseModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    @orm.reconstructor
    def __init__(self):
        self.fields = []

    def keys(self):
        return self.fields

    def __getitem__(self, item):
        return getattr(self, item)

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
