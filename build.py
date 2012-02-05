import os
from flask import Flask

import runserver

app = Flask(__name__)
app.config.from_envvar('SPHINXWEB_SETTINGS')

import shutil
from sphinx.util import copy_static_entry
from sphinx.websupport import WebSupport

try:
    os.makedirs(os.path.join(app.config['BUILD_DIR'], 'templates'))
except os.error:
    pass

support = WebSupport(srcdir=app.config['SOURCE_DIR'],
                     builddir=app.config['BUILD_DIR'],
                     storage=app.config['DATABASE_URI'])
support.build()

# copy resources from this webapp
for name in ['static', 'templates']:
    source_dir = os.path.join(os.getcwd(), 'sphinxweb', name)
    target_dir = os.path.join(app.config['BUILD_DIR'], name)
    copy_static_entry(source_dir, target_dir, None)

shutil.copy(os.path.join(os.getcwd(), 'sphinxweb', 'static',  'websupport.js'), os.path.join(app.config['BUILD_DIR'], 'static', '_static', 'websupport.js'))
