#!/usr/bin/env python
# -*- coding: utf-8 -*-

# all the imports
from black_star.sys.db import init_db

if __name__ == '__main__':
  print "Setting up database ... "
  init_db()
  print "DONE!"
