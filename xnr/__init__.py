# -*- coding: utf-8 -*-
from flask import Flask
from elasticsearch import Elasticsearch
from flask_debugtoolbar import DebugToolbarExtension
from xnr.extensions import admin
from xnr.index.views import mod as indexModule
from xnr.control.views import mod as controlModule
from xnr.personalCenter.views import mod as personalCenterModule
from xnr.registered.views import mod as registeredModule
from xnr.inforDetection.views import mod as inforDetectionModule
from xnr.monitor.views import mod as monitorModule
from xnr.behavioGauge.views import mod as behavioGaugeModule
from xnr.reportManage.views import mod as reportManageModule
from xnr.knowledge.views import mod as knowledgeModule
from xnr.systemManage.views import mod as systemManageModule
from xnr.system_manage.views import mod as systemmanageModule
from xnr.weibo_xnr_operate.views import mod as weiboxnroperateModule
from xnr.weibo_xnr_create.views import mod as weiboxnrcreateModule
from xnr.weibo_xnr_manage.views import mod as weiboxnrmanageModule
from xnr.weibo_xnr_assessment.views import mod as weiboxnrassessmentModule
from xnr.weibo_xnr_knowledge_base_management.views import mod as weiboxnrknowledgebasemanagementModule
from xnr.weibo_xnr_monitor.views import mod as weiboxnrmonitorModule
from xnr.weibo_xnr_warming.views import mod as weiboxnrwarmingModule
from xnr.weibo_xnr_warming_new.views import mod as weiboxnrwarmingnewModule
from xnr.weibo_xnr_report_manage.views import mod as weiboxnrreportmanageModule
from xnr.qq_xnr_manage.views import mod as qqxnrmanageModule
from xnr.qq_xnr_operate.views import mod as qqxnroperateModule
from xnr.qq_xnr_assessment.views import mod as qqxnrassessmentModule
from xnr.qq_xnr_monitor.views import mod as qqxnrmonitorModule
from xnr.qq_xnr_report_manage.views import mod as qqxnrreportmanageModule
from xnr.qq_xnr_warming.views import mod as qqxnrwarmingModule

from xnr.wx_xnr_manage.views import mod as wxxnrmanageModule
from xnr.wx_xnr_operate.views import mod as wxxnroperateModule
from xnr.wx_xnr_monitor.views import mod as wxxnrmonitorModule
from xnr.wx_xnr_assessment.views import mod as wxxnrassessmentModule
from xnr.wx_xnr_report_manage.views import mod as wxxnrreportmanageModule
from xnr.wx_xnr_warning.views import mod as wxxnrwarningModule

from xnr.facebook_xnr_warning.views import mod as facebookxnrwarningModule

from xnr.twitter_xnr_warning.views import mod as twitterxnrwarningModule

from xnr.facebook_xnr_operate.views import mod as facebookxnroperateModule
from xnr.twitter_xnr_operate.views import mod as twitterxnroperateModule

#from xnr.extensions import db, security, user_datastore, admin, User, Role, roles_users
from xnr.extensions import db, security, user_datastore, admin, User, Role, roles_users, AdminAccessView_user, AdminAccessView_role
#from flask.ext.security import SQLAlchemyUserDatastore
from flask_security import SQLAlchemyUserDatastore
from flask_admin.contrib import sqla
from xnr.jinja import gender, tsfmt, Int2string, gender_text, user_email, user_location, user_birth, user_vertify, weibo_source



def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///flask-admin.db'

    register_extensions(app)

    # Create modules
    #
    app.register_blueprint(indexModule)
    app.register_blueprint(controlModule)
    app.register_blueprint(personalCenterModule)
    app.register_blueprint(registeredModule)
    app.register_blueprint(inforDetectionModule)
    app.register_blueprint(monitorModule)
    app.register_blueprint(behavioGaugeModule)
    app.register_blueprint(reportManageModule)
    app.register_blueprint(knowledgeModule)
    app.register_blueprint(systemManageModule)
    app.register_blueprint(systemmanageModule)
    app.register_blueprint(weiboxnroperateModule)
    app.register_blueprint(weiboxnrcreateModule)
    app.register_blueprint(weiboxnrmanageModule)
    app.register_blueprint(weiboxnrassessmentModule)
    app.register_blueprint(weiboxnrknowledgebasemanagementModule)
    app.register_blueprint(weiboxnrmonitorModule)
    app.register_blueprint(weiboxnrwarmingModule)
    app.register_blueprint(weiboxnrwarmingnewModule)
    app.register_blueprint(weiboxnrreportmanageModule)
    app.register_blueprint(qqxnrmanageModule)
    app.register_blueprint(qqxnroperateModule)
    app.register_blueprint(qqxnrassessmentModule)
    app.register_blueprint(qqxnrmonitorModule)
    app.register_blueprint(qqxnrreportmanageModule)
    app.register_blueprint(qqxnrwarmingModule)
    app.register_blueprint(wxxnrmanageModule)
    app.register_blueprint(wxxnroperateModule)
    app.register_blueprint(wxxnrmonitorModule)
    app.register_blueprint(wxxnrassessmentModule)
    app.register_blueprint(wxxnrreportmanageModule)
    app.register_blueprint(wxxnrwarningModule)
    # the debug toolbar is only enabled in debug mode

    app.register_blueprint(facebookxnrwarningModule)

    app.register_blueprint(twitterxnrwarningModule)

    app.register_blueprint(facebookxnroperateModule)
    app.register_blueprint(twitterxnroperateModule)

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
    # debug toolbar
    # toolbar = DebugToolbarExtension(app)
    # app.config['MONGO_HOST'] = '219.224.134.212'
    # app.config['MONGO_PORT'] = 27017
    # app.config['MONGO_DBNAME'] = 'mrq'

    # init database
    db.init_app(app)
    with app.test_request_context():
        db.create_all()

    # init security
    security.init_app(app, datastore=user_datastore)

    # init admin
    admin.init_app(app)
    admin.add_view(AdminAccessView_user(User, db.session))
    admin.add_view(AdminAccessView_role(Role, db.session))
    # admin.add_view(sqla.ModelView(User, db.session))
    # admin.add_view(sqla.ModelView(Role, db.session))

    return app

def register_extensions(app):
    app.config.setdefault('ES_USER_PROFILE_URL', 'http://219.224.135.97:9208/')
    app.extensions['es_user_profile'] = Elasticsearch(app.config['ES_USER_PROFILE_URL'])
    app.config.setdefault('ES_USER_PORTRAIT_URL', 'http://219.224.135.93:9200/')
    app.extensions['es_user_portrait'] = Elasticsearch(app.config['ES_USER_PORTRAIT_URL'])

def register_jinja_funcs(app):
    funcs = dict(gender=gender,
                 tsfmt=tsfmt,
                 int2string=Int2string,
                 gender_text=gender_text,
                 user_email=user_email,
                 user_location=user_location,
                 user_birth=user_birth,
                 user_vertify=user_vertify,
                 weibo_source=weibo_source)
    app.jinja_env.globals.update(funcs)
