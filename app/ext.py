# coding=utf-8
from flask_mako import MakoTemplates, render_template  # noqa
from flask_sqlalchemy import SQLAlchemy,orm

mako = MakoTemplates()
db = SQLAlchemy()