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

@main.route('/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    user = User.query.get_or_404(id)
    
    if request.method == 'POST':
        user.nom = request.form['nom']
        user.email = request.form['email']
        user.mot_de_passe = request.form['mot_de_passe']
        user.isadmin = True if request.form.get('isadmin') == 'on' else False

        db.session.commit()
        return redirect(url_for('main.home'))

    return render_template('edit_user.html', user=user)

@main.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('main.home'))