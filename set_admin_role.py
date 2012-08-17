#!/usr/bin/env python

import sys
#from flask.ext.sqlalchemy import *
from runserver import app
from sphinxweb.views.docs import db, User

if len(sys.argv) != 3 or sys.argv[2] not in ['true', 'false']:
    print "Usage : ./set_admin_role.py <username> <true/false>"
    sys.exit(1)

username = sys.argv[1]
is_admin = sys.argv[2] == 'true'

user = User.query.filter_by(username=username).first()
if not user:
    print "%s does not exist in the database" % username
    sys.exit(1)

user.is_admin = is_admin
db.session.commit()
print "Successfully updated %s" % username