#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer,Float, String,MetaData ,ForeignKey,DateTime,Binary
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



engine = create_engine('sqlite:///:memory:', echo=True)   

metadata = MetaData()

user=Table('user',metadata,
    Column('id',Integer, autoincrement=True,primary_key=True),
    Column('user_tag',String),
    Column('password',String),
    Column('email',String),
    Column('status',String))
     
    
commentaire=Table( 'commentaire',metadata,
    Column('id',Integer,autoincrement=True, primary_key=True),
    Column('contenu',String),
    Column('score',Integer),
    Column('refere',Integer) ,
    Column('time',DateTime),
    Column('idUser',Integer, ForeignKey("user.id")),
    Column('idTopic',Integer, ForeignKey("topic.id"))
) 
topic=Table('topic',metadata,
    Column('id',Integer,autoincrement=True,primary_key=True),
    Column('nb_reponses',Integer),
    Column('contenu',Binary)
)

matiere=Table('matiere',metadata,
    Column('id' ,Integer,autoincrement=True, primary_key=True),
    Column('total_size',Float),
    Column('weekly_score',Integer)
)
        
file=Table('file',metadata,
    Column('id',Integer,autoincrement=True, primary_key=True),
    Column('size',Float),
    Column('data',Binary),
    Column('file_type',String),
    Column('idMatiere',Integer, ForeignKey("matiere.id"))
)
    

metadata.create_all(engine)                               
connection = engine.connect()