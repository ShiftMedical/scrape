from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

import settings

DeclarativeBase = declarative_base()

def db_connect():

    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))

def create_deals_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


class Deals(DeclarativeBase):
    """Sqlalchemy deals model"""
    __tablename__ = "deals"

    pid = Column(Integer, primary_key=True)
    id = Column('id', String, nullable=True)
    title = Column('title', String)
    link = Column('link', String, nullable=True)
    loc = Column('loc', String, nullable=True)
    email = Column('email', String, nullable=True)
    #job_desc = Column('job_desc', String, nullable=True)
    recruiter_notice = Column('recruiter_notice', String, nullable=True)
    services_notice = Column('services_notice', String, nullable=True)
    job_type = Column('job_type', String, nullable=True)
    date_created = Column('data_created', String, nullable=True)
    comp = Column('comp', String, nullable=True)
