# -*- coding: utf-8 -*-
from functools import wraps
from flask import Flask, request, Response
from flask import Module, render_template, request, g, abort, jsonify
from sphinx.websupport.errors import UserNotAuthorizedError, \
     DocumentNotFoundError

from sphinxweb import support
from sphinx.websupport.storage.sqlalchemy_db import Session, Comment
from sqlalchemy import desc

app = Flask(__name__)
app.config.from_envvar('SPHINXWEB_SETTINGS')

docs = Module(__name__)


def get_users(str):
    user_dict = {}
    users = app.config[str]
    for user in users.split("\n"):
        if user:
            username, password = user.split()
            user_dict[username] = password

    return user_dict

users = get_users('USERS')
admin_users = get_users('ADMIN_USERS')
users.update(admin_users)


def is_admin(username):
    return username in admin_users.keys()


def check_auth(username, password):
    return users.get(username) and users[username] == password


def check_admin(username, password):
    return admin_users.get(username) and admin_users[username] == password


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your credentials.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


def requires_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_admin(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@docs.route('/')
@requires_auth
def index():
    return doc('')


@docs.route('/<path:docname>/')
@requires_auth
def doc(docname):
    try:
        document = support.get_document(docname)
    except DocumentNotFoundError:
        abort(404)
    return render_template('doc.html', document=document)


@docs.route('/_get_comments')
@requires_auth
def get_comments():
    username = request.authorization.username
    node_id = request.args.get('node', '')
    data = support.get_data(node_id)
    comments = data.get('comments')
    if comments and not is_admin(username):
        # Show comments only by current user.
        data['comments'] = [comment for comment in comments if comment['username'] == username]

    return jsonify(**data)


@docs.route('/_add_comment', methods=['POST'])
@requires_auth
def add_comment():
    parent_id = request.form.get('parent', '')
    node_id = request.form.get('node', '')
    text = request.form.get('text', '')
    proposal = request.form.get('proposal', '')
    comment = support.add_comment(text, node_id, parent_id,
                                  displayed=True,
                                  username=request.authorization.username,
                                  proposal=proposal)
    return jsonify(comment=comment)


@docs.route('/comments')
@requires_admin
def all_comments():
    comments = Session().query(Comment).order_by(desc("id")).all()
    return render_template('comments.html', comments=comments)
