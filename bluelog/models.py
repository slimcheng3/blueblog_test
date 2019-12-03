# -*- coding: utf-8 -*-
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from bluelog.extensions import db


class Blogger(db.Model, UserMixin):
    __tablename__ = 'blogger'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    title = db.Column(db.Enum(
        '博客专家', '博客牛人', '博客新人', '游客'
    ), server_default='游客')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    blogger_id = db.Column(db.Integer, db.ForeignKey('blogger.id'))

    blogger = db.relationship('Blogger', backref='article')
    comments = db.relationship('Comment', backref='article', cascade='all, delete-orphan')


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))

