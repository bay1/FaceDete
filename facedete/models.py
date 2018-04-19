# coding=utf-8
from datetime import datetime
from .extensions import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    student_num = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(20))
    group = db.Column(db.String(20))
    log_id = db.Column(db.String(20))
    signlogs = db.relationship('Signlog', backref='user')

    def __repr__(self):
        return "<user %r>" % self.name


class Signlog(db.Model):
    __tablename__ = 'signlog'
    id = db.Column(db.Integer, primary_key=True)
    user_student_num = db.Column(db.Integer, db.ForeignKey('user.id'))
    ip = db.Column(db.String(20))
    pc_name = db.Column(db.String(20))
    signtime = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return "<signlog %r>" % self.id
