# -*- coding: utf-8 -*-
from flask import Module, render_template, request, g, abort, jsonify
from sphinx.websupport.errors import UserNotAuthorizedError, \
     DocumentNotFoundError

from sphinxweb import support
from sphinx.websupport.storage.sqlalchemy_db import Session, Comment
from sqlalchemy import desc


docs = Module(__name__)

@docs.route('/')
def index():
    return doc('')


@docs.route('/<path:docname>/')
def doc(docname):
    try:
        document = support.get_document(docname)
    except DocumentNotFoundError:
        abort(404)
    return render_template('doc.html', document=document)


@docs.route('/_get_comments')
def get_comments():
    node_id = request.args.get('node', '')
    data = support.get_data(node_id)
    return jsonify(**data)


@docs.route('/_add_comment', methods=['POST'])
def add_comment():
    parent_id = request.form.get('parent', '')
    node_id = request.form.get('node', '')
    author = request.form.get('author', '')
    text = request.form.get('text', '')
    proposal = request.form.get('proposal', '')
    comment = support.add_comment(text, node_id, parent_id,
                                  displayed=True,
                                  username=author,
                                  proposal=proposal)
    return jsonify(comment=comment)


@docs.route('/comments')
def all_comments():
    comments = Session().query(Comment).order_by(desc("id")).all()
    return render_template('comments.html', comments=comments)
