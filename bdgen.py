#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import datetime
from sqlalchemy import *
from sqlalchemy.sql import *
from sqlalchemy import exc
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer,Float, String,MetaData ,ForeignKey,DateTime,Binary



engine = create_engine('sqlite:///base.db', echo=False)   

metadata = MetaData()

user=Table('user',metadata,
    Column('email',String,nullable=False,primary_key=True),
    Column('user_tag',String),
    Column('password',String),
    Column('status',String))
      
commentaire=Table( 'commentaire',metadata,
    Column('id',Integer,autoincrement=True, primary_key=True),
    Column('contenu',String),
    Column('score',Integer),
    Column('refere',Integer) ,
    Column('time',DateTime,default=datetime.datetime.utcnow),
    Column('idUser',Integer, ForeignKey("user.email")),
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




'''
*******METHODES D'INSERTION******* 
'''
'''
ajouter_matiere ajoute une matière, equivalent à un insert
mais je l'ai fait pour toi
'''
def ajouter_matiere(nom_mat,conn):
    mat_ins = matiere.insert()
    conn.execute(mat_ins.values(nom_matiere=nom_mat,weekly_score=0))

'''
En gros pour ajouter un fichier il faut le convertire en binary object
c'est un peu chiant, ça a l'air de marcher
j'ai mis un try catch comme ça si le fichier disparaît balec
'''
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
        return False 

'''
Pour l'insertion d'un comm y'a plusieurs trucs à faire,
parce que les comms changent le ranking des matières

'''
def ajouter_comm(contenu,idUser,idTopic,refere,conn):
    comm_ins = commentaire.insert()
    conn.execute(comm_ins.values(contenu=contenu,refere=refere,idUser=idUser,idTopic=idTopic,score=0))
    
'''
Column('id',Integer, autoincrement=True,primary_key=True),
    Column('user_tag',String),
    Column('password',String),
    Column('email',String),
    Column('status',String))
    pour ajouter un user il faut voir si l'email et/ou le tag sont pas deja pris
'''

def ajouter_user(user_tag,password,email,status,conn):
    try:
        usr_ins = user.insert()
        conn.execute(usr_ins.values(user_tag=user_tag,password=password,email=email,status=status))
        return True
    except exc.SQLAlchemyError:
        print("couldnt add !")
        return False
  
'''
*******METHODES D'ACQUISITION*******
'''
'''
Lister_fich_mat liste tous les fichiers d'une matiere
surement utile pour les menus déroulants
'''
def lister_fich_mat(mat, conn):
    rowlist= []
    for row in connection.execute("select nom_fichier,id from file where id_matiere="+str(mat)):
        rowlist.append(row)
        print(row)
    return rowlist
'''
lister_reponses liste toutes les reponses à un commentaire(refere dans commentaire)    rowlist= []
surement utile l'affichage des commz à côté d'un sujet ou dans un topic honorable
mis dans l'ordre chronologique

'''
def lister_reponses(id_com,conn):
    rowlist= []
    for row in connection.execute("select * from commentaire where refere="+str(id_com)+" order by time asc"):
        rowlist.append(row)
        print(row)
    return rowlist
  
'''
Pour voir si un utilisateur existe vraiment
renvoie booleen
peut être utile pour la connection
'''
def user_exists(tag_or_email,password,conn):
    rowlist= []
    for row in connection.execute("select * from user where email="+str(tag_or_email)+"or user_tag="+str(tag_or_email)+"and password="+str(password)):
        rowlist.append(row)
    if(len(rowlist)==0):
        return False
    else:
        return True

metadata.create_all(engine)                               
connection = engine.connect() 

if  __name__=='__main__':#All test code goes here 
    ajouter_matiere("WEB",connection)
    ajouter_matiere("CRO",connection)
    ajouter_matiere("TSA",connection)
    
    ajouter_fichier("/home/tom/Documents/certificate.pdf","sujet de web",1,connection)
    ajouter_user("test","p","tom@qqch","dieu",connection)
    ajouter_user("max","p","max@lol","dieu",connection)
    ajouter_user("raph","p","tom@qqch","dieu",connection)
    

    