from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from main import create_app

app = create_app()
# app.config[
#     'SQLALCHEMY_DATABASE_URI'] = 'mysql+cymysql://root:123456@localhost/fisher'

from app.ext import db

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
