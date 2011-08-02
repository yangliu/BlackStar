#!/usr/bin/env python
# -*- coding: utf-8 -*-

from black_star import app, render_template, session, request, url_for, redirect
from black_star.sys.db import db_session
#from sqlalchemy.exc import OperationalError
from sqlalchemy.exc import DatabaseError

from black_star.sys.models import UFile
from black_star import config
import logging

@app.errorhandler(404)
def not_found_page(error):
  return render_template('err.html', title="Page Not Found", errtext="BlackStar can't find that page."), 404
  
@app.errorhandler(403)
def access_denied_page(error):
  return render_template('err.html', title="Access Denied", errtext="BlackStar can't serve this file to you."), 403
  

@app.errorhandler(DatabaseError)
def database_error_page(error):
  return render_template('err.html', title="Database Error", errtext="BlackStar can't connect to the database."), 500