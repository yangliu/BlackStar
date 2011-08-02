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
  