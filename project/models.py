from project.db import db
from flask_login import UserMixin
from sqlalchemy.sql import func



class Notes(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    data = db.Column(db.String(20000))
    created_date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    f_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    notes = db.relationship('Notes')