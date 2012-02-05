import sys
import os

THIS_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, THIS_DIR + '/..')

os.environ['SPHINXWEB_SETTINGS'] = os.path.join(THIS_DIR, '..', 'settings.py')

from sphinxweb import app as application
