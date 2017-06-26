# -*- coding: utf-8 -*-

import flask_security
from flask_login import current_user
from flask import g, session, flash, redirect, request, render_template
from flask_security.utils import logout_user
from optparse import OptionParser
from xnr import create_app
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
            UserMixin, RoleMixin, login_required
from xnr.extensions import db, user_datastore

optparser = OptionParser()
optparser.add_option('-p', '--port', dest='port', help='Server Http Port Number', default=9001, type='int')
(options, args) = optparser.parse_args()

# Create app
app = create_app()

# Create user role data to test with
@app.route('/create_user_role_test')
def create_user_roles():
    try:
        db.create_all()
        #role_1 = user_datastore.create_role(name='userrank', description=u'用户排行模块权限')
        user_1 = user_datastore.create_user(email='admin@qq.com', password="Bh123456")

        #user_datastore.add_role_to_user(user_1, role_1)
        #user_datastore.add_role_to_user(user_1, role_2)
        db.session.commit()
        return "success"
    except:
        db.session.rollback()
        return "failure"

@app.before_request
def before_request():
    g.user = current_user

@app.after_request
def after_request(response):
    return response

@app.route('/')
@login_required
def homepage():
    return render_template('homepage.html')

# logout
@app.route('/logout/')
@login_required
def logout():
    logout_user()
    #flash(u'You have been signed out')
    flash(u'登出成功')

    return redirect("/login") #redirect(request.args.get('next', None))

# app run
app.run(host='0.0.0.0', port=options.port)
