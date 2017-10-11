# -*- coding: utf-8 -*-

import flask_admin as admin
from flask_admin.contrib import sqla
from flask import request, redirect, url_for, flash
#from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
# from flask.ext.security import Security, SQLAlchemyUserDatastore, \
#             UserMixin, RoleMixin
from flask_security import Security, SQLAlchemyUserDatastore, \
            UserMixin, RoleMixin,current_user
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.fields import PasswordField
from wtforms import form, fields, validators

__all__ = ['admin']


# Create database connection object
db = SQLAlchemy()

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class AdminAccessView_user(sqla.ModelView):

    column_exclude_list = ('password',)#remove password column in list view
    column_labels = dict(department=u'部门')
    form_excluded_columns = ('password',)#remove password column in create view
    column_searchable_list = ('email',)
    column_auto_select_related = True

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('administration'):
            return True

        return False

    def scaffold_form(self):
        # Start with the standard form as provided by Flask-Admin. We've already told Flask-Admin to exclude the
        # password field from this form.
        form_class = super(AdminAccessView_user, self).scaffold_form()
        # Add a password field, naming it "password2" and labeling it "New Password".
        form_class.password2 = PasswordField(u'密码')
        return form_class

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                flash(u"没有权限访问该模块")
                return redirect("/")
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


    def on_model_change(self, form, model, is_created):
        # If the password field isn't blank...
        if len(model.password2):
            # ... then encrypt the new password prior to storing it in the database. If the password field is blank,
            # the existing password in the database will be retained.
            model.password = generate_password_hash(model.password2)
    # def on_model_change(self, form, User, is_created):
    #     User.password = form.password_hash.data

class AdminAccessView_role(sqla.ModelView):
    #column_exclude_list = ('password',)#remove password column in list view
    form_excluded_columns = ('password',)#remove password column in create view
    column_auto_select_related = True
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('administration'):
            return True

        return False

    #def on_model_change(self, form, User, is_created):
    #   User.password = form.password_hash.data
    def scaffold_form(self):
        # Start with the standard form as provided by Flask-Admin. We've already told Flask-Admin to exclude the
        # password field from this form.
        form_class = super(AdminAccessView_role, self).scaffold_form()
        # Add a password field, naming it "password2" and labeling it "New Password".
        form_class.password2 = PasswordField(u'密码')
        return form_class

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                flash(u"没有权限访问该模块")
                return redirect("/")
            else:
                # login
                return redirect(url_for('security.login', next=request.url))
    
    def on_model_change(self, form, model, is_created):
        # If the password field isn't blank...
        if len(model.password2):
            # ... then encrypt the new password prior to storing it in the database. If the password field is blank,
            # the existing password in the database will be retained.
            model.password = generate_password_hash(model.password2)

class Role(db.Model, RoleMixin):
    """用户角色
    """
    id = db.Column(db.Integer(), primary_key=True)
    # 该用户角色名称
    name = db.Column(db.String(80), unique=True)
    chname = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __unicode__(self):
        return self.name

    def __name__(self):
        return u'角色管理'

# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(255), unique=True)
#     password = db.Column(db.String(255))
#     active = db.Column(db.Boolean())
#     user_confirmedat  = db.Column(db.DateTime())
#     roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
#     usernum = db.Column(db.Integer)
#     moodnum = db.Column(db.Integer)
#     netnum = db.Column(db.Integer)
#     findnum = db.Column(db.Integer)
#     analysisnum = db.Column(db.Integer)
#     sensingnum = db.Column(db.Integer)
#     department = db.Column(db.String(255))
#     # Required for administrative interface. For python 3 please use __str__ instead.
#     def __unicode__(self):
#         return self.email

#     def __name__(self):
#         return u'用户管理'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    department = db.Column(db.String(255))
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    
    # usernum = db.Column(db.Integer)
    # moodnum = db.Column(db.Integer)
    # netnum = db.Column(db.Integer)
    # findnum = db.Column(db.Integer)
    # analysisnum = db.Column(db.Integer)
    # sensingnum = db.Column(db.Integer)

    # Required for administrative interface. For python 3 please use __str__ instead.
    def __unicode__(self):
        return self.email

    def __name__(self):
        return u'用户管理'

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security()

# Create admin
#admin = admin.Admin(name=u'权限管理', template_mode='bootstrap3')
admin = admin.Admin(name=u'权限管理', template_mode='role')
#admin = admin.Admin(name=u'权限管理', base_template='/portrait/role_manage.html')
