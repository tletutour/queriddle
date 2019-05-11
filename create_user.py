import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *

engine = create_engine('sqlite:///base.db', echo=True)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()

user = Utilisateur(username="Raphael",password="Monin", email="raphael.monin@insa-lyon.fr")
session.add(user)
user = Utilisateur(username="Marlon-Bradley",password="Paniah", email="to complete")
session.add(user)
user = Utilisateur(username="Maxime",password="Bernard", email="to complete")
session.add(user)
user = Utilisateur(username="Tom",password="Ltr", email="to complete")#j'ai changé mon mdp batar
session.add(user)
user = Utilisateur(username="Basile",password="Deneire", email="to complete")
session.add(user)

matieres3A=["WEB","TSA","CRO"]
matieres4A=["LOL","JSP","MDR"]
matieres5A=["BAH","STAGE","FDP"]
for mat in matieres3A:
    new_mat=Matiere(annee=3,nomMat=mat)
    session.add(new_mat)
for mat in matieres4A:
    new_mat=Matiere(annee=4,nomMat=mat)
    session.add(new_mat)
for mat in matieres5A:
    new_mat=Matiere(annee=5,nomMat=mat)
    session.add(new_mat)
#user = User("jumpiness","python")
#session.add(user)

# commit the record the database
session.commit()

