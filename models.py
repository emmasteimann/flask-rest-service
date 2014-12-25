from app import db
from flask import json
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy

class JsonSerializable(object):
    @property
    def columns(self):
        return [ c.name for c in self.__table__.columns ]

    @property
    def columnitems(self):
        return dict([ (c, getattr(self, c)) for c in self.columns ])

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.columnitems)

    def tojson(self):
        return self.columnitems

class Group(db.Model, JsonSerializable):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    users = association_proxy('group_users', 'user')

    def __init__(self, name):
        self.name = name


class User(db.Model, JsonSerializable):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    userid = db.Column(db.String, nullable=False, unique=True)
    groups = association_proxy('user_groups', 'group')

    def __init__(self, first_name, last_name, userid):
        self.first_name = first_name
        self.last_name = last_name
        self.userid = userid

class UserGroup(db.Model, JsonSerializable):
    __tablename__ = 'user_groups'
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    user = relationship(User, backref=backref("user_groups",
                                cascade="all, delete-orphan")
            )
    group = relationship(Group, backref=backref("group_users",
                                cascade="all, delete-orphan")
            )
    def __init__(self, user=None, group=None):
        self.user = user
        self.group = group
