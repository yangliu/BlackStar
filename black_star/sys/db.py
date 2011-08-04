#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer

from black_star import config


engine = create_engine('sqlite:///%s'%config.DATABASE, convert_unicode=True, echo=config.DEBUG)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

dbModel = declarative_base()
dbModel.query = db_session.query_property()


class DBVersion(dbModel):
  __tablename__ = 'db_version'
  version       = Column(Integer, primary_key=True)
  
  def __init__(self, version=None):
    self.version = version


def init_db():
  # import all modules here that might define models so that they will be registered properly on the metadata.  Otherwise you will have to import them first before calling init_db()
  import black_star.sys.models
  from black_star.sys.models import DB_MODELS_VERSION
  engine.echo = False
  dbModel.metadata.create_all(bind=engine)
  
  if DBVersion.query.count() == 0:
    #new install
    print "Creating database... "
    rec = DBVersion(version=DB_MODELS_VERSION)
    db_session.add(rec)
    db_session.commit()
  else:
    db_ver_rec = DBVersion.query.first()
    db_ver = db_ver_rec.version
    if db_ver < DB_MODELS_VERSION:
      print "Upgrading database… "
      for i in range(db_ver+1, DB_MODELS_VERSION+1):
        db_up(i)
        
      db_ver_rec.version = DB_MODELS_VERSION
      db_session.add(db_ver_rec)
      db_session.commit()





def db_up(ver):
  '''Database upgrader'''
  import sqlite3
  import os
  from black_star import app
  from contextlib import closing
  #####
  # From 1000 to 1001
  #  - UFile
  #    (*add)  Column('expire_at', DateTime)
  #####

  print "Upgrading %d ==> %d…" % (ver-1, ver)
  with closing(sqlite3.connect(os.path.join(config.ROOT_PATH, config.DATABASE))) as db:
    with app.open_resource('sqls/schema.%d.sql'%ver) as f:
      line = f.read()
      db.cursor().executescript(line)
      #print line
    db.commit()        