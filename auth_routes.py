#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, request, redirect, \
    url_for, flash, render_template, session, abort
from flask_mail import Mail, Message
from flask_socketio import SocketIO
import os
from random import choice
from string import ascii_lowercase
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from tabledef import Matiere, create_engine,Fichier, Utilisateur, RaphMail, \
    hasher, Tchat

#Génération base données
engine = create_engine('sqlite:///base.db', echo=True)

app = Flask(__name__)
socketio = SocketIO(app)


'''ROOT : Page Racine qui redirige vers login si non connecté, et vers ressources (resources)
sinon (ici, c'est le tchat)'''
@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('do_admin_login'))
    else:
        #return render_template('session.html', myUsername=session['username'])
        return redirect(url_for('resources'))


'''LOGIN : Page où l'on entre les identifiants (pseudo et mdp). On peut accéder à la page
permettant de créer un compte depuis ici'''
@app.route('/login', methods=['GET','POST'])
def do_admin_login():
    if request.method == 'POST':
        POST_USERNAME = str(request.form['username'])
        POST_PASSWORD = str(request.form['password'])
        password_hash = hasher(POST_PASSWORD)
        #Session sqlalchemy
        Session = sessionmaker(bind=engine)
        s = Session()
        #Requêtes SQL à la table users
        query = s.query(Utilisateur).filter(Utilisateur.username.in_([POST_USERNAME]),
                                            Utilisateur.password.in_([password_hash]))
        if query.first():
            session['logged_in'] = True
            session['username'] = POST_USERNAME
        else:
            flash("L'identifiant ou le mot de passe est incorrect")
        return redirect(url_for('home'))
    return render_template('login.html')


'''NEW_ACCOUNT : Autorisation pour créer un nouveau compte si l'adresse mail 
est validée'''
@app.route('/new_account', methods=['GET','POST'])
def new_account():
    if request.method == 'POST':
        #Check si l'email existe déjà
        Session = sessionmaker(bind=engine)
        s = Session()
        query = s.query(RaphMail.email).filter(RaphMail.email.in_([request.form['email']]))
        if query.first():
            flash("Cette adresse mail est déjà utilisée !")
            return redirect(url_for('new_account'))
        #Envoie l'email
        mail_settings = {
            "MAIL_SERVER": 'smtp.gmail.com',
            "MAIL_PORT": 465,
            "MAIL_USE_TLS": False,
            "MAIL_USE_SSL": True,
            "MAIL_USERNAME": "queriddle@gmail.com",
            "MAIL_PASSWORD": "Fullstack69!",
        }
        app.config.update(mail_settings)
        mail = Mail(app)
        key = "".join(choice(ascii_lowercase) for i in range(10))
        msg = Message(subject="Mail de confirmation - Queriddle",
                      sender=app.config.get("MAIL_USERNAME"),
                      recipients=[request.form['email']],
                      body="Bienvenue sur Queriddle ! Suis ce lien pour créer ton compte : http://127.0.0.1:5000/create_account/"+key)
        mail.send(msg)
        #Stockage des données
        user2 = RaphMail(key_email=str(key), email=str(request.form['email']))
        s.add(user2)
        s.commit()
        return render_template('login.html')
        #return redirect(url_for('mail_sent', envoi='mail_envoye'))
    return render_template('new_account.html')


'''CREATE_ACCOUNT : Une fois son adresse INSA confirmée, l'utilisateur va pouvoir choisir son pseudo 
et son mot de passe'''
@app.route('/create_account/<string:key>', methods=['GET','POST'])
def create_account(key):
    if request.method == 'POST':

        Session = sessionmaker(bind=engine)
        s = Session()
        #Check si l'username existe déjà
        query = s.query(Utilisateur.username).filter(Utilisateur.username.in_([request.form['username']]))
        if query.first():
            flash("Ce nom d'utilisateur existe déjà !")
            return redirect(url_for('create_account'))

        #Récupération de l'adresse mail entrée
        query = s.query(RaphMail.email).filter(RaphMail.key_email.in_([key]))
        user = Utilisateur(username=str(request.form['username']), password=str(request.form['password']),
                           email=str(query.first()[0]))

        s.add(user)
        s.commit()
        return redirect(url_for('do_admin_login'))
    return render_template('create_account.html', key = key)

def messageReceived(methods=['GET', 'POST']):
    print('------> LOG : message was received!!!')

'''Création du SOCKET et gestion des interactions'''
@socketio.on('my event')
def handle_my_custom_event(msg, methods=['GET', 'POST']):
    Session = sessionmaker(bind=engine)
    s = Session()
    print('------> LOG : received my event: ' + str(msg))
    socketio.emit('my response', msg, callback=messageReceived)
    new_message=Tchat(username = session['username'],refere = 0,contenu = msg["message"],idFichier = 0)#contenu,refere,username,idFichier,score=0
    s.add(new_message)
    s.commit()


#---------------Routes Statiques----------------------

'''RESOURCES : Accès à la page des ressources. Cette page affichera le pdf 
décrivant Queriddle'''
@app.route('/resources/')
def resources():
    #On liste toutes les années
    if not session.get('logged_in'):
        return redirect(url_for('do_admin_login'))
    else:
        anneeList=[]
        Session = sessionmaker(bind=engine)
        s = Session()
        #On affiche toutes les annees dispo
        #SELECT annee FROM Matiere GROUP BY annee
        query=s.query(Matiere.annee).group_by(Matiere.annee).all()
        for row in query:
            anneeList.add(row.annee)
    return render_template('resources.html',anneeList=anneeList)


'''RES.../NUM_ANNEE : En sélectionnant l'année dans le menu déroulant, la page 
recharge'''
@app.route('/resources/<int:num_annee>/')
def annee(num_annee):
    if not session.get('logged_in'):
        return redirect(url_for('do_admin_login'))
    else:
        matiereList=[]
        scoreList=[]
        Session = sessionmaker(bind=engine)
        s = Session()
        #On veut recup toutes les matières d'une année en particulier
        #On met les matières trending en premier
        #SELECT nomMat, score FROM Matiere WHERE annee=num_annee ORDER BY score DESC
        query=s.query(Matiere.nomMat, Matiere.score).filter_by(annee=num_annee).order_by(desc(Matiere.score)).all()
        for row in query:
            matiereList.add(row.nomMat)
            scoreList.add(row.score)
    return render_template('annee.html',matiereList=matiereList, scoreList=scoreList)


'''RES.../NUM_A.../MATIERE : Après choix de la matière dans le menu déroulant'''
@app.route('/resources/<int:num_annee>/<string:matiere>')
def matiere(num_annee, matiere):
    if not session.get('logged_in'):
        return redirect(url_for('do_admin_login'))
    else:
        fichierList=[]
        Session = sessionmaker(bind=engine)
        s = Session()
        #SELECT nomFichier FROM Fichier,Matiere
        #WHERE Matiere.id= Fichier.idMatiere AND Matiere.nomMat=matiere
        query=s.query(Fichier.nomFichier).join(Matiere).filter(Matiere.id==Fichier.idMatiere).filter(Matiere.nomMat==matiere).all()
        for row in query:
            fichierList.add(row.nomFichier)
    return render_template('matiere.html',fichierList=fichierList)


'''MY ACCOUNT : Accès à son espace personnel, d'où on pourra changer pseudo et mdp'''
@app.route('/myaccount/')
def myaccount():
    return render_template('myaccount.html')


'''LOG_OUT : Déconnexion de l'utilisateur'''
@app.route("/logout")
def logout():
    session['logged_in'] = False
    session.pop('username', None)
    return redirect(url_for('home'))



#------------GESTION DES PAGES D'ERREUR------------------------

@app.errorhandler(404)
def page_404(error):
    return render_template('404.html')




if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    socketio.run(app, debug=True, host='127.0.0.1', port=5000)

