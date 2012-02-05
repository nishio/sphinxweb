import os
THIS_DIR = os.path.abspath(os.path.dirname(__file__))
os.environ['SPHINXWEB_SETTINGS'] = os.path.join(THIS_DIR, 'settings.py')

from sphinxweb import app

if __name__ == '__main__':
    app.run()
