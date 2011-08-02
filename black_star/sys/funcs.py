#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, stat, sys
from black_star import config
from black_star import session


try:
  import magic
except:
  magic = None
  import mimetypes

def fullname(filename):
  return os.path.normpath(os.path.join(config.ROOT_PATH, config.UPLOAD_FILE_PATH, filename))

def f_exists(filename):
  if '..' in filename or filename.startswith('/'):
    return False
  f = fullname(filename)
  return os.path.exists(f)

def get_name_from_filename(filename):
  if "." not in filename:
    return filename
  else:
    return filename.rsplit('.', 1)[0]
    
def get_file_size(filename):
  f = fullname(filename)
  return os.path.getsize(f)
  
def get_file_mimetype(filename):
  f = fullname(filename)
  if magic is not None:
    mime = magic.Magic(mime=True)
    return mime.from_file(f)
  else:
    t, e = mimetypes.guess_type(f)
    return t
    
def is_admin_login():
  return 'username' in session and session['username'] == config.USERNAME