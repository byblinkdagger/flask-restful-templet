from flask import Flask as _Flask
from .ext import db, mako
from flask.json import JSONEncoder as _JSONEncoder
from app.model.collection import Collection

# for upload file
from werkzeug.wsgi import SharedDataMiddleware
from app.util.file_utils import get_file_path


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)


class Flask(_Flask):
    json_encoder = JSONEncoder


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.setting')
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/i/': get_file_path()
    })
    mako.init_app(app)
    db.init_app(app)
    register_app(app)
    with app.app_context():
        # db.drop_all()
        db.create_all()
        #
        # collection1 = Collection()
        # collection1.name = 'iphone'
        # db.session.add(collection1)
        #
        # collection2 = Collection()
        # collection2.name = 'artifact'
        # db.session.add(collection2)

        db.session.commit()

    return app


def register_app(app):
    from app.api.api import api
    app.register_blueprint(api)


if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=8088, debug=True)
