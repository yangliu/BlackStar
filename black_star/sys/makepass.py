#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import choice
import string
import hashlib
from black_star import config

def gen_passwd(length=8, chars=string.letters+string.digits):
  return ''.join([choice(chars) for i in range(length)])
  
def enc_passwd(code):
  return "%s%s"%(config.SALT, hashlib.sha1(code).hexdigest())
  
def sf_cookie_name(filename):
  return hashlib.sha1("%s%s"%(filename, config.SF_SALT)).hexdigest()
  
def sf_cookie_val(filename, code):
  return hashlib.sha1("%s%s%s"%(code, config.SF_SALT, filename)).hexdigest()