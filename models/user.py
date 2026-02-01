from flask_sqlalchemy import SQLAlchemy

from extensions.db import DB as db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100),)
    email = db.Column(db.String(50), unique=True, )
    password = db.Column(db.String(100),)
    is_admin = db.Column(db.Boolean, default=False)
