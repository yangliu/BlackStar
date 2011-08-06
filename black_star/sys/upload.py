#!/usr/bin/env python
# -*- coding: utf-8 -*-

from black_star import app, render_template, session, request, url_for, redirect, flash, abort, make_response
from werkzeug import secure_filename
from black_star.sys.db import db_session
from black_star.sys.models import UFile
from black_star.sys import funcs
from black_star.sys.makepass import gen_passwd, enc_passwd, sf_cookie_name, sf_cookie_val
from black_star.sys.plupload_backend import upload as plupload
from black_star import config
from datetime import datetime, timedelta
import os
import logging
import re
from hashlib import sha1
import glob
import shutil

@app.route('/upload/', methods=['GET', 'POST'])
def upload_page():
  if not funcs.is_admin_login(): abort(403)
  
  if request.method == 'POST':
    print request.form
    groupkey = request.form.get('groupkey', None)
    if groupkey is None: abort(403)
    try:
      file_num = int(request.form.get('file_num'))
    except:
      abort(403)
    if file_num <= 0: abort(403)
    
    def get_orig_filename(filename, group_key):
      pos = filename.rfind('-%s'%group_key)
      if pos != -1:
        return filename[:pos]
      else:
        return filename
      
    upload_dir = os.path.join(config.ROOT_PATH, config.UPLOAD_FOLDER)
    files = glob.glob(os.path.join(upload_dir, '*-%s'%groupkey))
    if not files: abort(403)
    elif len(files) == 1:
      o_fn = os.path.basename(get_orig_filename(files[0], groupkey))
      dst_fn = gen_dfn_filename(o_fn)
      
      shutil.copy(files[0], dst_fn)
      os.remove(files[0])
      d_fn = gen_file_item(dst_fn, o_fn)
      
      return redirect(url_for('edit_file', file_indicator=d_fn))
    else:
      o_fn = 'ziparchive.zip'
      o_f_type = 'zip'
      dst_fn = gen_dfn_filename(o_fn)
      d_fn = os.path.basename(dst_fn)
      d_basefn = d_fn[:d_fn.rfind('.')]
      newdir = os.path.join(upload_dir, d_basefn)
      os.mkdir(newdir)
      for f in files:
        o_fn = os.path.basename(get_orig_filename(f, groupkey))
        new_o_fn = os.path.join(newdir, o_fn)
        shutil.copy(f, new_o_fn)
        os.remove(f)
      shutil.make_archive(dst_fn[:dst_fn.rfind('.')], o_f_type, newdir)
      shutil.rmtree(newdir, True)
      
      d_fn2 = gen_file_item(dst_fn, '[Archive]%s'%datetime.utcnow().strftime('%Y-%m-%d %H:%I'))
      return redirect(url_for('edit_file', file_indicator=d_fn2))
  
  randkey = "%s-%s"%(sha1(str(datetime.utcnow())).hexdigest(), gen_passwd(8))
  return render_template('upload.html', title="Upload Files", randkey = randkey)

def gen_dfn_filename(fn):
  pos = fn.rfind('.')
  if pos != -1:
    fn_ext = fn[pos:]
  else:
    fn_ext = ''
  dst_fn = os.path.join(config.ROOT_PATH, config.UPLOAD_FILE_PATH, "%s%s"%(gen_passwd(5), fn_ext))
  while (os.path.exists(dst_fn)):
    dst_fn = os.path.join(config.ROOT_PATH, config.UPLOAD_FILE_PATH, "%s%s"%(gen_passwd(5), fn_ext))
  return dst_fn 

def gen_file_item(realfile, o_filename):
  pos = o_filename.rfind('.')
  if pos != -1:
    ufile_name = o_filename[:pos]
  else:
    ufile_name = o_filename
  d_fn = os.path.basename(realfile)
  
  ufile = UFile(
            name = ufile_name,
            url = d_fn,
            filename = d_fn,
            filesize = funcs.get_file_size(d_fn),
            mimetype = funcs.get_file_mimetype(d_fn),
            created = datetime.utcnow()
          )
  db_session.add(ufile)
  db_session.commit()
  return d_fn
   
  
@app.route('/upload/receive_file/', methods=['GET', 'POST'])
def upload_file_receiver():
  if not funcs.is_admin_login(): abort(403)
  return plupload(request)