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

# Email Templates
# Available fields: username, email_id, url, comment
COMMENT_NOTIFICATION_SUBJECT = u"New comment from {username}"
COMMENT_NOTIFICATION_BODY = u"{username} ({email_id}) added a new comment to {url} \n\n {comment}"

# Available fields: username, email_id, app_name, server_name
SIGNUP_EMAIL_SUBJECT = u"Welcome to {app_name}"
SIGNUP_EMAIL_BODY = u"Thanks for signing up in {app_name}. Your username is {username}. You can access the service at http://{server_name}"
SIGNUP_ADMIN_EMAIL_SUBJECT = u"New signup - {username}"
SIGNUP_ADMIN_EMAIL_BODY = u"{username} ({email_id}) signed up in {app_name}"


try:
    from production_settings import *
except ImportError:
    pass
