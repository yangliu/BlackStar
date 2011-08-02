#!/usr/bin/env python
# -*- coding: utf-8 -*-

from black_star import app, render_template, session, request, url_for, redirect, flash
from black_star.sys.db import db_session
from black_star.sys.models import UFile
from black_star import config
from hashlib import sha1
import logging

@app.route('/login/', methods=['GET', 'POST'])
def login_page():
  redirect_to = request.values.get('next', url_for('homepage'))
  print redirect_to
  if request.method == 'POST':
    u_name = request.form.get('username', None)
    u_pass = request.form.get('password', None)
    if u_name == config.USERNAME and sha1(u_pass).hexdigest() == config.PASSWORD:
      session['username'] = u_name
      if request.form.get('keeplog', None) == 'yes':
        session.permanent = True
      else:
        session.permanent = False
      return redirect(redirect_to)
    else:
      flash('Username or password is not valid.')
  
  return render_template('login.html', redirect_to=redirect_to)

@app.route('/logout/')
def logout_page():
  redirect_to = request.args.get('next', url_for('homepage'))
  session.pop('username', None)
  return redirect(redirect_to)
