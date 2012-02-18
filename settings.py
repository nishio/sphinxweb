import os
SETTINGS_DIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SOURCE_DIR = os.path.join(SETTINGS_DIR, 'doc')
BUILD_DIR = os.path.join(SETTINGS_DIR, 'build')
DATABASE_URI = 'sqlite:///' + os.path.join(SETTINGS_DIR, 'comments.db')
SECRET_KEY = ''
SEARCH = ''

# One account per line. Separate username and password by space.
USERS = """
john secret
bob abcdef
mary xyz
"""

ADMIN_USERS = """
admin secret
admin1 secret1
"""
