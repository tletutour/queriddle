from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///base.db', echo=True)
Base = declarative_base()

########################################################################
class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

class RaphMail(Base):

    __tablename__ = "raphmails"

    key_email = Column(String, primary_key=True)
    email = Column(String)

#----------------------------------------------------------------------
def __init__(self, username, password, email):

    self.username = username
    self.password = password
    self.key_email = key_email
    self.email = email

# create tables
Base.metadata.create_all(engine)
