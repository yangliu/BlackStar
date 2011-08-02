#!/usr/bin/env python
# -*- coding: utf-8 -*-

from black_star import app, render_template, session, request
from black_star.sys.db import db_session
from black_star.sys.models import UFile
from black_star import config
import logging
import math

@app.route('/recent/')
@app.route('/recent/<int:page_cur>')
def recent_files(page_cur = None):
  if page_cur is None: page_cur = 1
  file_num = UFile.query.filter(UFile.homeshow == True).count()
  page_num = int(math.ceil(float(file_num)/float(config.ITEMS_PER_PAGE)))
  if page_num <= 0: abort(404)
  all_pages = range(1, page_num+1)
  if page_cur not in all_pages: abort(404)
  
  files = UFile.query.filter(UFile.homeshow == True).order_by(UFile.created.desc()).limit(config.ITEMS_PER_PAGE).offset((page_cur-1)*config.ITEMS_PER_PAGE).all()
  
  page_title = "Recent Files (Page %d/%d)" % (page_cur, page_num)
  return render_template('list.html', title=page_title, all_pages=all_pages, page_cur=page_cur, files=files)


