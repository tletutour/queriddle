#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, request, redirect, \
    url_for, flash, render_template, make_response, session
from werkzeug.utils import secure_filename
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
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
        return render_template('index.html')


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
    return render_template('resources.html')

#... selon l'année choisie...
@app.route('/resources/<int:num_annee>/')
def annee():
    return render_template('annee.html')

@app.route('/resources/<int:num_annee>/<str:matiere>')
def matiere():
    return render_template('matiere.html')

#Espace personnel
@app.route('/myaccount/')
def myaccount():
    return render_template('myaccount.html')



if __name__ == "__main__":
    app.run()
