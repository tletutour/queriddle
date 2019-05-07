from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import os
from flask_mail import Mail
from sqlalchemy.orm import sessionmaker
from tabledef import *
engine = create_engine('sqlite:///base.db', echo=True)
mail = Mail()

app = Flask(__name__)
mail.init_app(app)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('do_admin_login'))
    else:
        return "Hello Boss!  <a href='/logout'>Logout</a>"

@app.route('/login', methods=['GET','POST'])
def do_admin_login():
    if request.method == 'POST':
        POST_USERNAME = str(request.form['username'])
        POST_PASSWORD = str(request.form['password'])

        Session = sessionmaker(bind=engine)
        s = Session()
        query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]))
        result = query.first()
        if result:
            session['logged_in'] = True
        else:
            flash('Mot de passe incorrect !')
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/create_account', methods=['GET','POST'])
def account():
    if request.method == 'POST':

        Session = sessionmaker(bind=engine)
        s = Session()
        #TODO verifier adresse INSA
        query = s.query(User.email).filter(User.email.in_([request.form['email']]))
        if query.first():
            flash("Ce nom d'utilisateur existe déjà !")
            return redirect(url_for('account'))
        else:
            msg = Message("Hello",
                      sender="queriddle@gmail.com",
                      recipients=["tom.le-tutour@insa-lyon.fr"])
            mail.send(msg)
        
        user = User(username=str(request.form['username']), password=str(request.form['password']))
        s.add(user)
        s.commit()
        return redirect(url_for('do_admin_login'))
    return render_template('create_account.html')

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=3000)