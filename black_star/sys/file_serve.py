#!/usr/bin/env python
# -*- coding: utf-8 -*-

from black_star import app, render_template, session, request, url_for, redirect, flash, abort, make_response
from flask import Markup
from black_star.sys.db import db_session
from black_star.sys.models import UFile
from black_star.sys import funcs
from black_star.sys.makepass import gen_passwd, enc_passwd, sf_cookie_name, sf_cookie_val
from black_star.chardet.universaldetector import UniversalDetector
from black_star import config
from datetime import datetime, timedelta
from hashlib import sha1
import os
import logging
import re

@app.route('/randlink/', methods=['POST'])
def rand_link():
  return gen_passwd(5)

@app.route('/delete/<file_indicator>')
def delete_file(file_indicator=None):
  if not funcs.is_admin_login(): abort(403)
  ufile = UFile.query.filter(UFile.url == file_indicator).first()
  if not ufile: abort(404)
  
  fn = funcs.fullname(ufile.filename)
  db_session.delete(ufile)
  db_session.commit()
  try:
    os.remove(fn)
  except:
    pass
  return redirect(url_for('file_serve',file_indicator=file_indicator))

@app.route('/<file_indicator>', methods = ['GET', 'POST'])
def file_serve(file_indicator = None):
  if file_indicator is None: return homepage()
  
  ufile = _get_ufile(file_indicator)
  preview = _get_preview(ufile)
  fileext = _get_fileext(ufile) 
  
  # unlock password protection file
  if funcs.is_admin_login(): ufile.password = ''
  if ufile.password and request.method == 'POST':
      password = request.form.get('p-word')
      if ufile.password == password: ufile.password = ''
  if ufile.password:
    preview = 'icon'
    fileext = 'secret'
  
  # is_expired
  if isinstance(ufile.expire_at, datetime):
    ufile.is_expired = ufile.expire_at < datetime.utcnow()
  else:
    ufile.is_expired = False
  
  visitkey = gen_passwd()
  
  page_title = ufile.name
  
  #beautiful filename
  pos = ufile.filename.rfind('.')
  if pos != -1:
    ufile.beautiful_filename = "%s%s" % (ufile.name, ufile.filename[pos:])
  else:
    ufile.beautiful_filename = ufile.name
  
  response = make_response(render_template('file.html', ufile=ufile, preview = preview, fileext = fileext, file_indicator = file_indicator, visitkey=visitkey, edit_page = True, title=page_title))
  if not ufile.password and not ufile.is_expired:
    response.set_cookie(sf_cookie_name(ufile.filename), sf_cookie_val(ufile.filename, visitkey))
  else:
    response.set_cookie(sf_cookie_name(ufile.filename), "")
  
  return response  

@app.route('/edit/<file_indicator>', methods = ['GET', 'POST'])
def edit_file(file_indicator = None):
  if request.method == 'GET' and file_indicator is None: return homepage()
  if not funcs.is_admin_login(): 
    abort(403)
  
  ufile = None
  if request.method == 'POST':
    try:
      ufile = UFile.query.filter(UFile.id == int(request.form.get('file_id'))).first()
    except:
      ufile = None
    
    if not ufile:
      abort(403)
    err = False
    
    name = Markup(request.form.get('name')).striptags().strip()
    if not name:
      err = True
      flash('Title is empty or contains illegal characters.')
    else:
      ufile.name = name
    
    url = re.sub('[^%a-zA-Z0-9_\-\.]', '', request.form.get('url')).strip('-')
    if not url:
      err = True
      flash('URL is empty or contains illegal characters.')
    else:
      ufile.url = url
      if UFile.query.filter(UFile.url == 'url').count() > 0:
        err = True
        flash('URL has already existed.')
      
    ufile.password = request.form.get('password').strip()
    if not ufile.password: ufile.password = None
    
    ufile.description = request.form.get('description').strip()
    if not ufile.description: ufile.description = None
    
    try:
      expire_delta = int(request.form.get('expire_delta'))
    except:
      expire_delta = -1
    if expire_delta == -1:
      pass
    else:
      if expire_delta == 0:
        ufile.expire_at = None
      else:
        ufile.expire_at = datetime.utcnow()+timedelta(hours=expire_delta)
    
    for item in ['linkable', 'download', 'homeshow']:
      if request.form.get(item) == 'yes':
        setattr(ufile, item, True)
      else:
        setattr(ufile, item, False)
    
    if not err:
      db_session.add(ufile)
      try:
        db_session.commit()
        return redirect(url_for('file_serve',file_indicator=url))
      except:
        flash('Failed to update database.')
    
    
    
  if ufile is None: ufile = _get_ufile(file_indicator)
  preview = _get_preview(ufile)
  fileext = _get_fileext(ufile) 
  
  visitkey = gen_passwd()
  
  page_title = "Edit \"%s\"" % ufile.name
  
  if ufile.description is None: ufile.description = ''
  if ufile.password is None: ufile.password = ''
  
  response = make_response(render_template('edit.html', ufile=ufile, preview = preview, fileext = fileext, file_indicator = file_indicator, visitkey=visitkey, edit_page = False, title=page_title))
  response.set_cookie(sf_cookie_name(ufile.filename), sf_cookie_val(ufile.filename, visitkey))
  return response  


def _get_ufile(file_indicator = None):
  ufile = UFile.query.filter(UFile.url == file_indicator).first()
  if not ufile:
    ufile = None
  
  if ufile is not None:
    # test whether file exists
    if not funcs.f_exists(ufile.filename):
      db_session.delete(ufile)
      db_session.commit()
      abort(404)
  else:
    if not funcs.f_exists(file_indicator):
      abort(404)
    
    ufile = UFile(
              name = funcs.get_name_from_filename(file_indicator),
              url = file_indicator,
              filename = file_indicator,
              filesize = funcs.get_file_size(file_indicator),
              mimetype = funcs.get_file_mimetype(file_indicator),
              created = datetime.utcnow()
            )
    db_session.add(ufile)
    db_session.commit()
    #if not r:
    #  logging.error('Failed to commit new record: %r' % ufile)
    #  abort(404)
  return ufile

def _get_preview(ufile):
  # deal with the preview
  if ufile.mimetype in ['image/jpeg', 'image/png', 'image/bmp', 'image/gif']:
    preview = 'image'
  elif ufile.mimetype in ['text/plain']:
    preview = 'text'
    enc_detector = UniversalDetector()
    file_lines = []
    try:
      with open(funcs.fullname(ufile.filename), 'r') as f:
        for line in f:
          file_lines.append(line)
          if not enc_detector.done:
            enc_detector.feed(line)
      enc_detector.close()
      def unicodefy(s):
        return unicode(s, enc_detector.result.get('encoding'), errors='ignore')
      file_lines = map(unicodefy, file_lines)
      ufile.file_content = '<p>%s</p>' % '</p><p>'.join(file_lines)
    except:
      ufile.file_content = 'failed to open file'
      
    
    
  else:
    preview = 'icon'
  return preview
  
def _get_fileext(ufile):
  if '.' in ufile.filename:
    fileext = ufile.filename.rsplit('.', 1)[1].lower()
  else:
    fileext = '<NONE>'
  return fileext