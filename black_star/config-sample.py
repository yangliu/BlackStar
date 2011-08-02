#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Site Name
SITE_NAME = "BlackStar File Server"

# Host
HOST = '0.0.0.0'
PORT = 9876
URL_ROOT = 'http://localhost:9876'

# viewable exts
VIEWABLE_EXTS = [
  'pdf', 
  'jpg', 'jpeg', 'jpe', 'gif', 'bmp', 'png', 
  'mp3', 
  'html', 'htm', 'xml', 
  'flv', 'swf'
]

# max width and height of pictures in preview page
UFILE_PIC_MAX_WIDTH = 496
UFILE_PIC_MAX_HEIGHT = 496

# items per page in recent item page
ITEMS_PER_PAGE = 15

# Filename of SQL Database
DATABASE = 'black_star/test_database.sqlite3'

# Switch of Debug mode
DEBUG = False

# the name of session cookie
SESSION_COOKIE_NAME = 'sess_black_star_s'
# A timedelta which is used to set the expiration date of a permanent session.
from datetime import timedelta
PERMANENT_SESSION_LIFETIME = timedelta(days=62)

# The secret key for user sessions
# Please generate an random string on your own computer with following python code
# >>>import os
# >>>os.urandom(24)
# Copy and paste the string generated.
SECRET_KEY = "\xb1{\xc5\x1f\x10[/S'\x85\xa49u\x19\x13\xb0]2\x95\xf6,\xe9\xcbK"
SALT = 'SA'
SF_SALT = '1Q51oXdATZ'

# Admin username and password
USERNAME = 'admin'
# encoded password, for example, your password is 12345
# >>>import hashlib
# >>> hashlib.sha1('12345').hexdigest()
# '8cb2237d0679ca88db6464eac60da96345513964'
PASSWORD = '8cb2237d0679ca88db6464eac60da96345513964'

# Upload File path
UPLOAD_FILE_PATH = 'files'

# --------- please do not change them unless you know what you are doing --------
import os
# root path - DO NOT CHANGE
ROOT_PATH = os.getcwd()
