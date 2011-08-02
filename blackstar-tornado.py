#!/usr/bin/env python
# -*- coding: utf-8 -*-

# all the imports
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from werkzeug.contrib.fixers import ProxyFix
from blackstar import app
from black_star import config



if __name__ == '__main__':
  app.wsgi_app = ProxyFix(app.wsgi_app)
  http_server = HTTPServer(WSGIContainer(app))
  http_server.listen(config.PORT)
  IOLoop.instance().start()