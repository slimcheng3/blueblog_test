# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
import random

from faker import Faker

from bluelog import db
from bluelog.models import Blogger, Article, Comment

fake = Faker()


def fake_blogger():
    blogger = Blogger(
        username='slim',
        title='博客新人',
    )
    blogger.set_password('mimashi123')
    db.session.add(blogger)
    db.session.commit()


def fake_articles(count=50):
    for i in range(count):
        article = Article(
            title=fake.sentence(),
            body=fake.text(2000),
            blogger_id=1,
            timestamp=fake.date_time_this_year()
        )

        db.session.add(article)
    db.session.commit()


def fake_comments(count=500):
    for i in range(count):
        comment = Comment(
            author=fake.name(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            article=Article.query.get(random.randint(1, Article.query.count()))
        )
        db.session.add(comment)

    salt = int(count * 0.1)
    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            article=Article.query.get(random.randint(1, Article.query.count()))
        )
        db.session.add(comment)
    db.session.commit()
