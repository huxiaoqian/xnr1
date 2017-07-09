# -*- coding: utf-8 -*-

from flask import Flask
from elasticsearch import Elasticsearch
from flask_debugtoolbar import DebugToolbarExtension
from xnr.extensions import admin
from xnr.index.views import mod as indexModule
from xnr.weibo_xnr_operate.views import mod as weiboxnroperateModule
from xnr.weibo_xnr_create.views import mod as weiboxnrcreateModule
from xnr.weibo_xnr_manage.views import mod as weiboxnrmanageModule
from xnr.weibo_xnr_assessment.views import mod as weiboxnrassessmentModule
from xnr.weibo_xnr_monitor.views import mod as weiboxnrmonitorModule
from xnr.qq_xnr_manage.views import mod as qqxnrmanageModule
from xnr.qq_xnr_operate.views import mod as qqxnroperateModule
from xnr.qq_xnr_assessment.views import mod as qqxnrassessmentModule
from xnr.extensions import db, security, user_datastore, admin, User, Role, roles_users
from flask.ext.security import SQLAlchemyUserDatastore
from flask_admin.contrib import sqla

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///flask-admin.db'

    register_extensions(app)

    # Create modules
    app.register_blueprint(indexModule)
    app.register_blueprint(weiboxnroperateModule)
    app.register_blueprint(weiboxnrcreateModule)
    app.register_blueprint(weiboxnrmanageModule)
    app.register_blueprint(weiboxnrassessmentModule)
    app.register_blueprint(weiboxnrmonitorModule)
    app.register_blueprint(qqxnrmanageModule)
    app.register_blueprint(qqxnroperateModule)
    app.register_blueprint(qqxnrassessmentModule)
    # the debug toolbar is only enabled in debug mode
    app.config['DEBUG'] = True

    app.config['ADMINS'] = frozenset(['youremail@yourdomain.com'])
    app.config['SECRET_KEY'] = 'SecretKeyForSessionSigning'
    
    '''
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://%s:@%s/%s?charset=utf8' % (MYSQL_USER, MYSQL_HOST, MYSQL_DB)
    app.config['SQLALCHEMY_ECHO'] = False
    '''
    app.config['DATABASE_CONNECT_OPTIONS'] = {}

    app.config['THREADS_PER_PAGE'] = 8

    app.config['CSRF_ENABLED'] = True
    app.config['CSRF_SESSION_KEY'] = 'somethingimpossibletoguess'

    # Enable the toolbar?
    app.config['DEBUG_TB_ENABLED'] = app.debug
    # Should intercept redirects?
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
    # Enable the profiler on all requests, default to false
    app.config['DEBUG_TB_PROFILER_ENABLED'] = True
    # Enable the template editor, default to false
    app.config['DEBUG_TB_TEMPLATE_EDITOR_ENABLED'] = True
    
    # debug toolbar
    # toolbar = DebugToolbarExtension(app)

    # init database
    db.init_app(app)
    with app.test_request_context():
        db.create_all()

    # init security
    security.init_app(app, datastore=user_datastore)

    # init admin
    admin.init_app(app)
    admin.add_view(sqla.ModelView(User, db.session))
    admin.add_view(sqla.ModelView(Role, db.session))
    
    return app
   


def register_extensions(app):
    app.config.setdefault('ES_USER_PROFILE_URL', 'http://219.224.135.97:9208/')
    app.extensions['es_user_profile'] = Elasticsearch(app.config['ES_USER_PROFILE_URL'])
    app.config.setdefault('ES_USER_PORTRAIT_URL', 'http://219.224.135.93:9200/')
    app.extensions['es_user_portrait'] = Elasticsearch(app.config['ES_USER_PORTRAIT_URL'])

