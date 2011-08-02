#!/usr/bin/env python
# -*- coding: utf-8 -*-

VERSION = '1.0-dev'

# all the imports
import os
from flask import Flask, request, session, g, redirect, url_for, abort, flash, make_response
from flask import render_template as flask_render_template
from black_star.sys.db import db_session
from black_star.sys.makepass import gen_passwd
from black_star import config

app = Flask(__name__)
app.config.from_object(config)
app.config.from_envvar('BLACK_STAR_SETTINGS', silent=True)

@app.before_request
def create_session_identifier():
  if 'id' not in session:
    pass

@app.after_request
def change_server_str(response):
  response.headers['Server'] = "%s (%s)" % (config.SITE_NAME, config.URL_ROOT)
  response.headers['X-Powered-By'] = 'BlackStar/%s (%s)' % (VERSION, 'http://liuy.me/black-star')
  return response

@app.teardown_request
def shutdown_session(exception=None):
  db_session.remove()

from black_star.sys import filters
def render_template(template_name, **context):
  new_context = { 
      'config': config,
      'is_admin_login': 'username' in session and session['username'] == config.USERNAME
    }
  for k, v in context.iteritems():
    if k not in new_context:
      new_context[k] = v
  
  return flask_render_template(template_name, **new_context)


if __name__ == '__main__':
  app.run()