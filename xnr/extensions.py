# -*- coding: utf-8 -*-

import flask_admin as admin
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
            UserMixin, RoleMixin


__all__ = ['admin']


# Create database connection object
db = SQLAlchemy()

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    """用户角色
    """
    id = db.Column(db.Integer(), primary_key=True)
    # 该用户角色名称
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __unicode__(self):
        return self.name

    def __name__(self):
        return u'角色管理'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    # Required for administrative interface. For python 3 please use __str__ instead.
    def __unicode__(self):
        return self.email

    def __name__(self):
        return u'用户管理'

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security()

# Create admin
admin = admin.Admin(name=u'权限管理', template_mode='bootstrap3')
#admin = admin.Admin(name=u'权限管理', base_template='/portrait/role_manage.html')
