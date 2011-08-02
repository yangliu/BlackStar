#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, BigInteger, Integer, Boolean, String, Text, DateTime, PickleType, ForeignKey
from black_star.sys.db import dbModel

class UFile(dbModel):
  __tablename__ = 'ufiles'
  
  id            = Column(Integer, primary_key=True, autoincrement=True)
  name          = Column(String(200))
  url           = Column(String(200), unique=True)
  description   = Column(Text)
  created       = Column(DateTime)
  filename      = Column(String(255))
  filesize      = Column(BigInteger)
  mimetype      = Column(String(100))
  download      = Column(Boolean)
  linkable      = Column(Boolean(create_constraint=False))
  password      = Column(String(200))
  homeshow      = Column(Boolean)
  
  def __init__(self, name=None, url=None, description=None, created=None, filename=None, filesize=0, mimetype=None, download=True, linkable=False, password=None, homeshow=True):
  
    self.name = name 
    self.url = url
    self.description = description
    self.created = created
    self.filename = filename
    self.filesize = filesize
    self.mimetype = mimetype
    self.download = download
    self.linkable = linkable
    self.password = password
    self.homeshow = homeshow
    
    
  def __repr__(self):
    return '<UFile: Name: %r, Filename: %r>' % (self.name, self.filename)
    
  