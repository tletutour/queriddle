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
user = Utilisateur(username="Tom",password="Le Tutour", email="to complete")
session.add(user)
user = Utilisateur(username="Basile",password="Deneire", email="to complete")
session.add(user)

#user = User("jumpiness","python")
#session.add(user)

# commit the record the database
session.commit()

