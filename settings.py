import os
SETTINGS_DIR = os.path.abspath(os.path.dirname(__file__))

APP_NAME = "Sphinxweb"

DEBUG = True

SOURCE_DIR = os.path.join(SETTINGS_DIR, 'doc')
BUILD_DIR = os.path.join(SETTINGS_DIR, 'build')
DATABASE_URI = 'sqlite:///' + os.path.join(SETTINGS_DIR, 'comments.db')
SQLALCHEMY_DATABASE_URI = DATABASE_URI
SECRET_KEY = ''
SEARCH = ''

SERVER_NAME = 'localhost:5000'

# Set this to False to disable sending email notifications
EMAIL_ENABLED = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'example@gmail.com'
EMAIL_HOST_PASSWORD = 'a_secret_password'
EMAIL_SENDER = "%s <%s>" % (APP_NAME, EMAIL_HOST_USER)


try:
    from production_settings import *
except ImportError:
    pass
