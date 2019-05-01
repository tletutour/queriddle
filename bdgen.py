#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer,Float, String,MetaData ,ForeignKey,DateTime,Binary
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker




Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    user_tag =Column(String)
    password =Column(String)
    email =Column(String)
    status =Column(String)
     
    
class Commentaire(Base):
    __tablename__ = 'commentaire'
    id = Column(Integer, primary_key=True)
    contenu =Column(String)
    score =Column(Integer)
    refere=Column(Integer) 
    time=Column(DateTime)
    idUser=Column(Integer, ForeignKey("user.id"))
    idTopic=Column(Integer, ForeignKey("topic.id"))
    
    idUser = relationship("User")
    idTopic = relationship("Topic")
    
class Topic(Base):
    __tablename__="topic"
    id=Column(Integer,primary_key=True)
    nb_reponses=Column(Integer)
    contenu=Column(Binary)

class Matiere(Base):
    __tablename__="matiere"
    id = Column(Integer, primary_key=True)
    total_size=Column(Float)
    weekly_score=Column(Integer)
        
class File(Base):
    __tablename__="file"
    id = Column(Integer, primary_key=True)
    size=Column(Float)
    data=Column(Binary)
    file_type=Column(String)
    idMatiere=Column(Integer, ForeignKey("matiere.id"))
    
    idMatiere = relationship("Matiere")
    

engine = create_engine('sqlite:///sqlalchemy_example.db', echo=True)
Base.metadata = MetaData(engine)
session = sessionmaker(engine)()