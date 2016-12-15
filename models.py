#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app, db

posts_tags_table = db.Table(
    'posts_tags_table', db.Model.metadata,
    db.Column('post_id', db.String, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(250))
    tags = db.relationship('Tag', secondary=posts_tags_table)

    def __str__(self):
        return self.title

class Tag(db.Model):
    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    posts = db.relationship('Post', secondary=posts_tags_table)

    def __str__(self):
        return self.name
