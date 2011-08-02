#!/usr/bin/env python
# -*- coding: utf-8 -*-

from black_star import app, render_template, session, request, url_for, redirect, abort
from flask import send_from_directory
from black_star import config
from black_star.sys import funcs
from black_star.sys.makepass import sf_cookie_name, sf_cookie_val
from black_star.sys.models import UFile
import os, stat
from datetime import datetime, tzinfo

@app.route('/file/<filename>')
def static_file(filename = None):
  if not funcs.f_exists(filename): abort(404)
  
  key = request.args.get('key')
  v_key = request.cookies.get(sf_cookie_name(filename))
  if key and v_key and v_key == sf_cookie_val(filename, key):
    pass
  else:
    abort(403)
  
  is_download = request.args.get('download')
  if is_download == 'yes':
    #mimetype = 'application/octet-stream'
    mimetype = None
    as_attachment = True
  else:
    mimetype = None
    as_attachment = False
  
  return send_from_directory(os.path.normpath(os.path.join(config.ROOT_PATH, config.UPLOAD_FILE_PATH)), filename, mimetype=mimetype, as_attachment=as_attachment)

@app.route('/f<int:file_id>/<filename>')
def direct_file(file_id, filename):
  ufile = UFile.query.filter(UFile.id == file_id).first()
  if not ufile: abort(404)
  if not ufile.linkable: abort(403)
  
  if not funcs.f_exists(ufile.filename): abort(404)
  return send_from_directory(os.path.normpath(os.path.join(config.ROOT_PATH, config.UPLOAD_FILE_PATH)), filename)