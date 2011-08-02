#!/usr/bin/env python
# -*- coding: utf-8 -*-

from black_star import app, render_template, session, request
from black_star.sys.db import db_session
from black_star.sys.models import UFile
from black_star import config
import logging

@app.route('/')
def homepage():
  return render_template('homepage.html')


