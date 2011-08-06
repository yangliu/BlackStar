#!/usr/bin/env python
# -*- coding: utf-8 -*-

from black_star import app, render_template, session, request, url_for, redirect, abort
from flask import send_from_directory
from black_star import config
from black_star.sys import funcs
from black_star.sys.makepass import sf_cookie_name, sf_cookie_val
from black_star.sys.models import UFile
import os, stat
from datetime import datetime, tzinfo, timedelta

@app.route('/file<int:file_id>/<filename>')
def static_file(file_id=None, filename = None):
  #if not funcs.f_exists(filename): abort(404)
  ufile = UFile.query.filter(UFile.id == file_id).first()
  if not ufile: abort(404)
  if not funcs.f_exists(ufile.filename): abort(404)
  
  is_download = request.args.get('download')
  
  if is_download == 'yes':
    if not ufile.download: abort(403)
    as_attachment = True
    try:
      attachment_filename = filename.encode('UTF-8')
    except:
      attachment_filename = None
  else:
    as_attachment = False
    attachment_filename = None
  
  # reference
  if not as_attachment and request.referrer.startswith(config.URL_ROOT):
    self_ref = True
  else:
    self_ref = False
    
  key = request.args.get('key')
  v_key = request.cookies.get(sf_cookie_name(ufile.filename))
  if self_ref or (key and v_key and v_key == sf_cookie_val(ufile.filename, key)):
    pass
  else:
    abort(403)
  
  return send_from_directory(os.path.normpath(os.path.join(config.ROOT_PATH, config.UPLOAD_FILE_PATH)), ufile.filename, as_attachment=as_attachment, attachment_filename=attachment_filename)

@app.route('/f<int:file_id>/<filename>')
def direct_file(file_id, filename):
  ufile = UFile.query.filter(UFile.id == file_id).first()
  if not ufile: abort(404)
  if not ufile.linkable: abort(403)
  if isinstance(ufile.expire_at, datetime) and datetime.utcnow()>ufile.expire_at:
    abort(403)
  
  if not funcs.f_exists(ufile.filename): abort(404)
  return send_from_directory(os.path.normpath(os.path.join(config.ROOT_PATH, config.UPLOAD_FILE_PATH)), filename)