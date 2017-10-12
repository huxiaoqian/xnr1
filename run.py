# -*- coding: utf-8 -*-
import base64
import os
import json
import time
import sqlite
import sqlite3
import flask_security
from flask_login import current_user
from flask import g, session, flash, redirect, request, render_template
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename, SharedDataMiddleware
from flask_security.utils import logout_user
from optparse import OptionParser
from xnr import create_app
#from flask.ext.security import Security, SQLAlchemyUserDatastore, \
#            UserMixin, RoleMixin, login_required
from flask_security import Security, SQLAlchemyUserDatastore, \
            UserMixin, RoleMixin, login_required
#from flask.ext.login import LoginManager, login_user, login_required, logout_user, session, current_user
from flask_login import LoginManager, login_user, login_required, logout_user


from xnr.extensions import db, user_datastore
from xnr.time_utils import ts2datetime,datetime2ts
from xnr.global_utils import es_xnr,weibo_log_management_index_name,weibo_log_management_index_type


optparser = OptionParser()
optparser.add_option('-p', '--port', dest='port', help='Server Http Port Number', default=9001, type='int')
(options, args) = optparser.parse_args()

# Create app
app = create_app()

#
app.config['SECURITY_PASSWORD_SALT'] = 'salty'
app.config['SECURITY_LOGIN_USER_TEMPLATE'] = 'security/login_user.html'
# upload weibo images

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
APP_ROOT = os.path.dirname(os.path.abspath(__file__)) 
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'xnr/weibo_images/') 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print 'request::',request.files
        
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('uploaded_file',
            #                         filename=filename))
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            return path
    # return '''
    # <!doctype html>
    # <title>Upload new File</title>
    # <h1>Upload new File</h1>
    # <form action="" method=post enctype=multipart/form-data>
    #   <p><input type=file name=file>
    #      <input type=submit value=Upload>
    # </form>
    # '''

# Create user role data to test with
@app.route('/create_user_role_test/')
def create_user_roles():
    
    db.drop_all()

    try:
        db.create_all()
        role_1 = user_datastore.create_role(name='administration', description=u'超级管理员模块')
        user_1 = user_datastore.create_user(email='admin@qq.com', password="Bh123456",department=u'部门')
        #user_2 = user_datastore.create_user(email='admin2@qq.com', password="Bh123456")

        user_datastore.add_role_to_user(user_1, role_1)
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
    ip = request.remote_addr
    timestamp = int(time.time())
    user_name = ''
    _id = current_user.get_id()
    cx = sqlite3.connect("/home/ubuntu8/yuanhuiru/xnr/xnr1/xnr/flask-admin.db")
    #cx = sqlite3.connect("sqlite:///flask-admin.db")
    cu=cx.cursor()
    users = cu.execute("select id,email from user") 
    for row in users:
        if row[0] == int(_id):
            user_name = row[1]
            break
    cx.close()


    current_date = ts2datetime(timestamp)
    current_time_new = datetime2ts(current_date)

    log_id = user_name +'_'+ current_date
    
    
    exist_item = es_xnr.exists(index=weibo_log_management_index_name,doc_type=weibo_log_management_index_type,\
        id=log_id)

    if exist_item:
        get_result = es_xnr.get(index=weibo_log_management_index_name,doc_type=weibo_log_management_index_type,\
        id=log_id)['_source']

        login_ip_list = get_result['login_ip']
        login_time_list = get_result['login_time']

        login_ip_list.append(ip)
        login_time_list.append(timestamp)

        es_xnr.update(index=weibo_log_management_index_name,doc_type=weibo_log_management_index_type,\
        id=log_id,body={'doc':{'login_ip':login_ip_list,'login_time':login_time_list}})
    else:
        item_dict = {}
        item_dict['user_name'] = user_name
        item_dict['login_ip'] = [ip]
        item_dict['login_time'] = [timestamp]
        item_dict['operate_date'] = current_date
        item_dict['operate_time'] = current_time_new
        item_dict['user_id'] = ''
        item_dict['user_name'] = ''
        item_dict['operate_content'] = ''
        
        es_xnr.index(index=weibo_log_management_index_name,doc_type=weibo_log_management_index_type,\
            id=log_id,body=item_dict)

    return render_template('index/navigationMain.html')

# logout
@app.route('/logout/')
@login_required
def logout():
    logout_user()
    #flash(u'You have been signed out')
    flash(u'登出成功')

    return redirect("/login") #redirect(request.args.get('next', None))


# get ip
# @app.route('/get_ip/')
# def index():
#     user_name = ''
#     ip = request.remote_addr
#     _id = current_user.get_id()
#     cx = sqlite3.connect("/home/ubuntu8/yuanhuiru/xnr/xnr1/xnr/flask-admin.db")
#     #cx = sqlite3.connect("sqlite:///flask-admin.db")
#     cu=cx.cursor()
#     users = cu.execute("select id,email   from user") 
#     for row in users:
#         if row[0] == int(_id):
#             user_name = row[1]
#             break
#     cx.close()
#     return json.dumps([ip,user_name])

# get user 
@app.route('/get_user/')
def get_user():
    cx = sqlite3.connect("/home/ubuntu8/yuanhuiru/xnr/xnr1/xnr/flask-admin.db")
    #cx = sqlite3.connect("/home/user_portrait_0320/revised_user_portrait/user_portrait/user_portrait/flask-admin.db")
    cu=cx.cursor()
    cu.execute("select * from user") 
    user_info = cu.fetchall()
    cx.close()
    return json.dumps(user_info)

# app run
app.run(host='0.0.0.0', port=options.port)
