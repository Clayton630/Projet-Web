from flask import Blueprint, render_template, request, redirect, url_for
from .models import User
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    users = User.query.all()
    return render_template('home.html', users=users)

@main.route('/add_user', methods=['POST'])
def add_user():
    nom = request.form['nom']
    email = request.form['email']
    mot_de_passe = request.form['mot_de_passe']
    isadmin = True if request.form.get('isadmin') == 'on' else False

    new_user = User(nom=nom, email=email, mot_de_passe=mot_de_passe, isadmin=isadmin)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('main.home'))