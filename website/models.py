from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    sender = db.Column(db.Integer)
    reciever = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    chat_id = db.Column(db.String(32), db.ForeignKey('chat.id'))

class Chat(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    messages = db.relationship('Message')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    email = db.Column(db.String(128))
    password = db.Column(db.String(128))