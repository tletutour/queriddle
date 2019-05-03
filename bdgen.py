#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer,Float, String,MetaData ,ForeignKey,DateTime,Binary



engine = create_engine('sqlite:///base.db', echo=False)   

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
    Column('nom_matiere',String),
    Column('contenu',String),
    Column('score',Integer),
    Column('refere',Integer) ,
    Column('time',DateTime),
    Column('idUser',Integer, ForeignKey("user.id")),
    Column('contenu',String),
    Column('score',Integer),
    Column('refere',Integer) ,
    Column('time',DateTime),
    Column('idUser',Integer, ForeignKey("user.id")),
    Column('idTopic',Integer, ForeignKey("topic.id")),
    Column('weekly_score',Integer)
)
        
file=Table('file',metadata,
    Column('id',Integer,autoincrement=True, primary_key=True),
    Column('nom_fichier',String),
    Column('size',Float),
    Column('data',Binary,nullable=False),
    Column('file_type',String),
    Column('id_matiere',Integer, ForeignKey("matiere.id"))
)

def ajouter_matiere(nom_mat,conn):
    mat_ins = matiere.insert()
    conn.execute(mat_ins.values(nom_matiere=nom_mat,weekly_score=0))
"""  
def lister_fich_mat(id_mat, conn):
    resultat=.query    
"""    
def ajouter_fichier(filepath,nom_fich,id_mat,conn):
    fich_ins = file.insert()
    try:
        with open(filepath,'rb') as binary_file:
            print(type(binary_file))
            data = binary_file.read()
            conn.execute(fich_ins.values(nom_fichier=nom_fich,
                                         size=os.stat(filepath).st_size,
                                         data=data,
                                         file_type=None,
                                         id_matiere=id_mat))
            binary_file.close()
        return True
    except IOError:
        return False #Couldn't open File!
    
    

metadata.create_all(engine)                               
connection = engine.connect() 


ajouter_matiere("WEB",connection)
ajouter_matiere("CRO",connection)
ajouter_matiere("TSA",connection)
ajouter_fichier("/home/tom/Documents/certificate.pdf","sujet de web",1,connection)
for row in connection.execute("select * from file"):
    print(row)
print('\n')