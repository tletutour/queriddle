# -*- coding:utf-8 -*-
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from flask_mail import Mail, Message
from flask_socketio import SocketIO
import os
from random import choice
from string import ascii_lowercase
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from tabledef import Utilisateur, RaphMail,Matiere, hasher,Tchat
engine = create_engine('sqlite:///base.db', echo=True)

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('do_admin_login'))
    else:
        Session = sessionmaker(bind=engine)
        s = Session()
        query = s.query(Tchat.contenu, Tchat.username)
        messages = []
        for q in query:
            messages.append({"user_name": q[1], "message": q[0]})
        return render_template('session.html', myUsername=session['username'], messages = messages)

@app.route('/login', methods=['GET','POST'])
def do_admin_login():
    if request.method == 'POST':
        POST_USERNAME = str(request.form['username'])
        POST_PASSWORD = str(request.form['password'])
        password_hash=hasher(POST_PASSWORD)

        Session = sessionmaker(bind=engine)
        s = Session()
        query = s.query(Utilisateur).filter(Utilisateur.username.in_([POST_USERNAME]), Utilisateur.password.in_([password_hash]))
        result = query.first()
        if result:
            session['logged_in'] = True
            session['username'] = POST_USERNAME
        else:
            flash('Mot de passe incorrect !')
        return redirect(url_for('home'))
    return render_template('login.html')

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
        # On récupère l'adresse mail correspondante, qui doit forcement exister
        query = s.query(RaphMail.email).filter(RaphMail.key_email.in_([key]))
        user = Utilisateur(username=str(request.form['username']), password=str(request.form['password']), email=str(query.first()[0]))
        s.add(user)
        s.commit()
        return redirect(url_for('do_admin_login'))
    return render_template('create_account.html', key=key)

@app.route('/new_account', methods=['GET','POST'])
def new_account():
    if request.method == 'POST':
        #Check si l'email existe déjà
        Session = sessionmaker(bind=engine)
        s = Session()
        query = s.query(RaphMail.email).filter(RaphMail.email.in_([request.form['email']]))
        if query.first():
            flash("Cette adresse mail est déjà utilisé !")
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
        msg = Message(subject="Merci Marley !",
                      sender=app.config.get("MAIL_USERNAME"),
                      recipients=[request.form['email']],
                      body="Salut va sur ce lien pour creer ton compte : http://127.0.0.1:5000/create_account/"+key)
        mail.send(msg)
        # Stock les données
        user2 = RaphMail(key_email=str(key), email=str(request.form['email']))
        s.add(user2)
        s.commit()
        return render_template('login.html')
    return render_template('new_account.html')

@app.route("/logout")
def logout():
    session['logged_in'] = False
    session.pop('username', None)
    return redirect(url_for('home'))

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(msg, methods=['GET', 'POST']):
    Session = sessionmaker(bind=engine)
    s = Session()
    print('received my event: ' + str(msg))
    socketio.emit('my response', msg, callback=messageReceived)
    new_message=Tchat(username = session['username'],refere = 0,contenu = msg["message"],idFichier = 0)#contenu,refere,username,idFichier,score=0
    s.add(new_message)
    s.commit()
    
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    socketio.run(app, debug=True, host='127.0.0.1', port=5000)
