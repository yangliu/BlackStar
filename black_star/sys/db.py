#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from black_star import config




engine = create_engine('sqlite:///%s'%config.DATABASE, convert_unicode=True, echo=config.DEBUG)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

dbModel = declarative_base()
dbModel.query = db_session.query_property()

def init_db():
  # import all modules here that might define models so that they will be registered properly on the metadata.  Otherwise you will have to import them first before calling init_db()
  import black_star.sys.models
  dbModel.metadata.create_all(bind=engine)