from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String,DateTime,Binary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
import hashlib

engine = create_engine('sqlite:///base.db', echo=True)
Base = declarative_base()

########################################################################
class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

#----------------------------------------------------------------------
    def __init__(self, username, password):
    
        self.username = username
        self.password = password


class Utilisateur(Base):

    __tablename__ = "utilisateurs"
    id = Column(Integer, primary_key=True)
    email= Column(String)
    username = Column(String)
    password = Column(String)
    status= Column(String)
    
    def __init__(self, username, email,password):
    
        self.username = username
        self.email= email
        self.password = password
        self.status="normal"
    

class Matiere(Base):
    __tablename__="matieres"
    id=Column(Integer, primary_key=True)
    nomMat=Column(String)
    annee=Column(Integer)
    score=Column(Integer)
    
    
    def __init__(self, nomMat,annee):
        self.nomMat = nomMat
        self.score=0
        self.annee=annee
        
class Message(Base):
    __tablename__="messages"
    id=Column(Integer, primary_key=True)
    contenu= Column(String)
    score= Column(Integer)
    refere= Column(Integer)
    date= Column(DateTime)
    
    idUser=Column(Integer, ForeignKey("utilisateurs.id"))
    idFichier=Column(Integer, ForeignKey("fichiers.id"))
    
    user_rel=relationship("Utilisateur",foreign_keys=[idUser])
    fich_rel=relationship("Fichier",foreign_keys=[idFichier])
    

    
class Fichier(Base):
    __tablename__="fichiers"
    id=Column(Integer, primary_key=True)
    nomFichier= Column(String)
    contenu= Column(Binary)
    typeFichier=Column(String)
    
    idMatiere=Column(Integer, ForeignKey("matieres.id"))
    
    mat_rel=relationship("Matiere",foreign_keys=[idMatiere])
    
class QuestionArchive(Base):
    __tablename__="questionsArchivees"
    id=Column(Integer, primary_key=True)
    contenu=Column(String)
    
    idUser=Column(Integer, ForeignKey("utilisateurs.id"))
    idMatiere=Column(Integer, ForeignKey("matieres.id"))
    idFichier=Column(Integer, ForeignKey("fichiers.id"))
    
    user_rel=relationship("Utilisateur",foreign_keys=[idUser])
    mat_rel=relationship("Matiere",foreign_keys=[idMatiere])
    fich_rel=relationship("Fichier",foreign_keys=[idFichier])
    
class Commentaire(Base):
    __tablename__="commentaires"
    id=Column(Integer, primary_key=True)
    contenu=Column(String)
    
    idUser=Column(Integer, ForeignKey("utilisateurs.id"))
    idQuestArch=Column(Integer, ForeignKey("questionsArchivees.id"))
    
    user_rel=relationship("Utilisateur",foreign_keys=[idUser])
    user_rel=relationship("QuestionArchive",foreign_keys=[idQuestArch])



# create tables
Base.metadata.create_all(engine)