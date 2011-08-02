#!/usr/bin/env python
# -*- coding: utf-8 -*-

# all the imports
from black_star import app
from black_star import config

from black_star.sys import errorpages
from black_star.sys import homepage
from black_star.sys import listpage
from black_star.sys import login_page
from black_star.sys import file_serve
from black_star.sys import http_file


if __name__ == '__main__':
  app.run(host=config.HOST, port=config.PORT)