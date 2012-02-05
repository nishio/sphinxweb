# -*- coding: utf-8 -*-
import sys
from os import path

from flask import Flask, g, session, url_for

from sphinx.websupport import WebSupport

app = Flask(__name__)
app.config.from_envvar('SPHINXWEB_SETTINGS')
app.root_path = app.config['BUILD_DIR']

support = WebSupport(datadir=path.join(app.config['BUILD_DIR'], 'data'),
                     docroot='',
                     storage=app.config['DATABASE_URI'])

@app.context_processor
def inject_globalcontext():
    """Inject "sg", the global context."""
    return dict(sg=support.get_globalcontext())


from sphinxweb.views.docs import docs
app.register_module(docs)
