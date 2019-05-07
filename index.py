#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, request, redirect, \
    url_for, flash, render_template, make_response, session
from werkzeug.utils import secure_filename
import os
from sqlalchemy import desc
from sqlalchemy.orm import sessionmaker
from tabledef import Matiere, User, create_engine,Fichier,Utilisateur
engine = create_engine('sqlite:///base.db', echo=True)

app = Flask(__name__)
app.secret_key =  os.urandom(12)

#Page d'accueil
@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('do_admin_login'))
        #return render_template('index2.html')
    else:
        return render_template('resources.html')


#Page de login
@app.route('/login', methods=['GET','POST'])
def do_admin_login():
    if request.method == 'POST':
        POST_USERNAME = str(request.form['username'])
        POST_PASSWORD = str(request.form['password'])
        #Session sqlalchemy
        Session = sessionmaker(bind=engine)
        s = Session()
        #requêtes à la table users de la classe User de tabledef
        query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]))
        result = query.first()
        if result:
            session['logged_in'] = True
        else:
            flash("L'identifiant ou le mot de passe est incorrect")
        return redirect(url_for('index'))
    return render_template('login.html')


#Création de compte
@app.route('/create_account', methods=['GET','POST'])
def account():
    if request.method == 'POST':

        Session = sessionmaker(bind=engine)
        s = Session()

        query = s.query(User.username).filter(User.username.in_([request.form['username']]))
        if query.first():
            flash("Ce nom d'utilisateur existe déjà !")
            return redirect(url_for('account'))
        user = User(username=str(request.form['username']), password=str(request.form['password']))
        s.add(user)
        s.commit()
        return redirect(url_for('do_admin_login'))
    return render_template('create_account.html')

#Accès aux sujets, TDs ...
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

#... selon l'année choisie...
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

@app.route('/resources/<int:num_annee>/<string:matiere>')
def matiere(num_annee,matiere):
    if not session.get('logged_in'):
        return redirect(url_for('do_admin_login'))
    else:
        fichierList=[]
        Session = sessionmaker(bind=engine)
        s = Session()
        #SELECT nomFichier FROM Fichier,Matiere 
        #WHERE Matiere.id= Fichier.idMatiere AND Matiere.nomMat=matiere
        query=s.query(Fichier.nomFichier).join(Matiere).filter(Matiere.id=Fichier.idMatiere).filter(Matiere.nomMat=matiere).all()
        for row in query:
            matiereList.add(row.nomFichier)
    return render_template('matiere.html',fichierList=fichierList)

#Espace personnel
@app.route('/myaccount/')
def myaccount():
    return render_template('myaccount.html')



if __name__ == "__main__":
    app.run()
