# -*- coding: utf-8 -*-
from functools import wraps
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

import flask
from flask import Flask, request, Response
from flask import Module, render_template, request, g, abort, jsonify
from sphinx.websupport.errors import UserNotAuthorizedError, \
     DocumentNotFoundError

from sphinxweb import support
from sphinx.websupport.storage.sqlalchemy_db import Session, Comment
from sqlalchemy import desc
from flask.ext.sqlalchemy import *
from werkzeug import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config.from_envvar('SPHINXWEB_SETTINGS')
db = SQLAlchemy(app)

docs = Module(__name__)


class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    pwdhash = db.Column(db.String())
    email = db.Column(db.String(200), unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime)

    def __init__(self, username, password, email):
        self.username = username
        self.pwdhash = generate_password_hash(password)
        self.email = email
        self.created = datetime.utcnow()

    def __repr__(self):
        return '<User %r>' % self.username

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)


db.create_all()


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your credentials.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def check_auth(username, password, is_admin):
    user = User.query.filter_by(username=username).first()
    return user and user.check_password(password) and (not is_admin or user.is_admin == is_admin)


def requires_auth(admin=False):
    def _requires_auth(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth = request.authorization
            if not auth or not check_auth(auth.username, auth.password, is_admin=admin):
                return authenticate()
            return f(*args, **kwargs)
        return decorated
    return _requires_auth


def send_email(receivers, subject, body):
    if app.config['EMAIL_ENABLED']:
        msg = MIMEText(body.encode('utf-8'), 'plain', 'utf-8')
        msg['To'] = ", ".join(receivers)
        msg['From'] = app.config['EMAIL_SENDER']
        msg['Subject'] = subject

        server = smtplib.SMTP(app.config['EMAIL_HOST'], app.config['EMAIL_PORT'])
        server.starttls()
        server.login(app.config['EMAIL_HOST_USER'], app.config['EMAIL_HOST_PASSWORD'])
        server.sendmail(app.config['EMAIL_SENDER'], receivers, msg.as_string())
        server.quit()


def send_comment_notification(username, email_id, comment, url):
    receivers = User.query.filter_by(is_admin=True).all() or []
    receivers = [receiver.email for receiver in receivers]
    receivers.append(email_id)

    url = u"http://%s/%s" % (app.config['SERVER_NAME'], url)
    args = dict(username=username, email_id=email_id, comment=comment, url=url)
    body = app.config['COMMENT_NOTIFICATION_BODY'].format(**args)
    subject = app.config['COMMENT_NOTIFICATION_SUBJECT'].format(**args)

    send_email(receivers, subject, body)


def send_signup_notification(username, email_id):
    app_name = app.config['APP_NAME']
    server_name = app.config['SERVER_NAME']
    args = dict(username=username,
                email_id=email_id,
                app_name=app_name,
                server_name=server_name)

    # Notification to user
    receivers = [email_id]
    subject = app.config['SIGNUP_EMAIL_SUBJECT'].format(**args)
    body = app.config['SIGNUP_EMAIL_BODY'].format(**args)
    send_email(receivers, subject, body)

    # Notification to admins
    receivers = User.query.filter_by(is_admin=True).all() or []
    receivers = [receiver.email for receiver in receivers]
    subject = app.config['SIGNUP_ADMIN_EMAIL_SUBJECT'].format(**args)
    body = app.config['SIGNUP_ADMIN_EMAIL_SUBJECT'].format(**args)
    send_email(receivers, subject, body)


@docs.route('/')
@requires_auth()
def index():
    return doc('')


@docs.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        try:
            username = request.form['username']
            password = request.form['password']
            email_id = request.form['email']
            user = User(username, password, email_id)
            db.session.add(user)
            db.session.commit()
            send_signup_notification(username, email_id)
            return flask.redirect("/")
        except Exception as e:
            flask.flash("Sorry, there was an error! %s" % e, category="error")
            db.session.rollback()
    return render_template("signup.html")


@docs.route('/<path:docname>/')
@requires_auth()
def doc(docname):
    try:
        document = support.get_document(docname)
    except DocumentNotFoundError:
        abort(404)
    return render_template('doc.html', document=document)


@docs.route('/_get_comments')
@requires_auth()
def get_comments():
    username = request.authorization.username
    is_admin = User.query.filter_by(username=username).first().is_admin
    node_id = request.args.get('node', '')
    data = support.get_data(node_id)
    comments = data.get('comments')
    if comments and not is_admin:
        # Show comments only by current user.
        data['comments'] = [comment for comment in comments if comment['username'] == username]

    return jsonify(**data)


@docs.route('/_add_comment', methods=['POST'])
@requires_auth()
def add_comment():
    parent_id = request.form.get('parent', '')
    node_id = request.form.get('node', '')
    text = request.form.get('text', '')
    proposal = request.form.get('proposal', '')
    username = request.authorization.username
    email = User.query.filter_by(username=username).first().email
    comment = support.add_comment(text, node_id, parent_id,
                                  displayed=True,
                                  username=username,
                                  proposal=proposal)
    url = "%s#ao%s" % (comment['document'], comment['node'])
    send_comment_notification(username, email, text, url)
    return jsonify(comment=comment)


@docs.route('/comments')
@requires_auth(admin=True)
def all_comments():
    comments = Session().query(Comment).order_by(desc("id")).all()
    return render_template('comments.html', comments=comments)
