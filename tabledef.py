from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
import hashlib
import datetime

engine = create_engine('sqlite:///base.db', echo=True)
Base = declarative_base()


def hasher(mystring):
    hash_object = hashlib.md5(mystring.encode())
    return hash_object.hexdigest()


class Utilisateur(Base):

    __tablename__ = "utilisateurs"
    username = Column(String, primary_key=True)
    email= Column(String)

    password = Column(String)
    status= Column(String)
    
    def __init__(self, email,username,password):
        self.email=email
        self.username=username
        self.password=hasher(password)

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
 
class Tchat(Base):
    __tablename__="messages"
    id=Column(Integer, primary_key=True)
    contenu= Column(String)
    score= Column(Integer)
    refere= Column(Integer)
    date= Column(DateTime,default=datetime.datetime.utcnow)
    username=Column(Integer, ForeignKey("utilisateurs.username"))
    idFichier=Column(Integer, ForeignKey("fichiers.id"))
    
    user_rel=relationship("Utilisateur",foreign_keys=[username])
    fich_rel=relationship("Fichier",foreign_keys=[idFichier])
    
    def __init__(self, contenu,refere,username,idFichier,score=0):
        self.contenu=contenu
        self.score=score
        self.refere= refere
        self.username=username
        self.idFichier=idFichier

class Fichier(Base):
    __tablename__="fichiers"
    id=Column(Integer, primary_key=True)
    nomFichier= Column(String)
    contenu= Column(Binary)
    typeFichier=Column(String)
    
    idMatiere=Column(Integer, ForeignKey("matieres.id"))
    
    mat_rel=relationship("Matiere",foreign_keys=[idMatiere])
    
    def __init__(self,nomFichier,contenu,typeFichier,idMatiere):
        self.nomFichier=nomFichier
        self.contenu=contenu
        self.typeFichier=typeFichier
        self.idMatiere=idMatiere
        
class QuestionArchive(Base):
    __tablename__="questionsArchivees"
    id=Column(Integer, primary_key=True)
    contenu=Column(String)
    
    username=Column(Integer, ForeignKey("utilisateurs.username"))
    idMatiere=Column(Integer, ForeignKey("matieres.id"))
    idFichier=Column(Integer, ForeignKey("fichiers.id"))
    
    user_rel=relationship("Utilisateur",foreign_keys=[username])
    mat_rel=relationship("Matiere",foreign_keys=[idMatiere])
    fich_rel=relationship("Fichier",foreign_keys=[idFichier])
    
    def __init__(self,contenu,username,idMatiere,idFichier):
        self.contenu=contenu
        self.username=username
        self.idMatiere=idMatiere
        self.idFichier=idFichier
    
class Commentaire(Base):
    __tablename__="commentaires"
    id=Column(Integer, primary_key=True)
    contenu=Column(String)
    username=Column(Integer, ForeignKey("utilisateurs.username"))
    idQuestArch=Column(Integer, ForeignKey("questionsArchivees.id"))
    user_rel=relationship("Utilisateur",foreign_keys=[username])
    user_rel=relationship("QuestionArchive",foreign_keys=[idQuestArch])

    def __init__(self, contenu,username,idQuestArch):
        self.contenu=contenu
        self.username=username
        self.idQuestArch=idQuestArch
class RaphMail(Base):
    __tablename__="raphmails"
    #On met ça en primary pour être sur de chez sur
    #Que personne aura la même clé d'url
    key_email=Column(String,primary_key=True)
    email=Column(String)
    
    def __init__(self,key_email,email):
        self.key_email=key_email
        self.email=email
    


# create tables
Base.metadata.create_all(engine)
