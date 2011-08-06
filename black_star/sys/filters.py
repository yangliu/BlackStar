#!/usr/bin/env python
# -*- coding: utf-8 -*-

from black_star import app
from black_star.flaskext.markdown import Markdown

Markdown(app)


@app.template_filter('file_ext')
def file_ext(s):
  if '.' not in s:
    return 'NONE'
  return s.rsplit('.', 1)[1].upper()

@app.template_filter('bs_filesize')
def bs_filesize(s):
  try:
    size = int(s)
  except:
    return s
  
  if size > 1000*1000*1000*1000:
    return "%.1f %s" % (float(size)/float(1000*1000*1000*1000),'TB')
  elif size > 1000*1000*1000:
    return "%.1f %s" % (float(size)/float(1000*1000*1000),'GB')
  elif size > 1000*1000:
    return "%.1f %s" % (float(size)/float(1000*1000),'MB')
  elif size > 1000:
    return "%.1f %s" % (float(size)/float(1000),'KB')
  elif size > 1:
    return "%d %s" % size,'Bytes'
  else:
    return 'N/A'        
  
  