from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db

main = Blueprint('main', __name__)

# Redirection de l'URL racine vers la page de login
@main.route('/')
def index():
    return redirect(url_for('main.login'))

# Page d'accueil pour les admins
@main.route('/home')
@login_required
def home():
    if not current_user.isadmin:
        flash('Accès réservé aux administrateurs.', 'danger')
        return redirect(url_for('main.dashboard'))

    users = User.query.all()
    return render_template('home.html', users=users)

# Formulaire d'inscription
@main.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        nom = request.form['nom']
        email = request.form['email']
        mot_de_passe = request.form['mot_de_passe']
        isadmin = True if request.form.get('isadmin') == 'on' else False

        user = User.query.filter_by(email=email).first()
        if user:
            flash('L\'email est déjà utilisé.', 'danger')
            return redirect(url_for('main.add_user'))

        hashed_password = User.hash_password(mot_de_passe)
        User.add(nom, email, hashed_password, isadmin)
        flash('Compte créé avec succès !', 'success')
        return redirect(url_for('main.login'))

    return render_template('add_user.html')

# Modification utilisateur
@main.route('/edit_user/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    user = User.query.get_or_404(id)

    if request.method == 'POST':
        nom = request.form['nom']
        email = request.form['email']
        mot_de_passe = request.form['mot_de_passe']
        isadmin = True if request.form.get('isadmin') == 'on' else False

        if mot_de_passe:
            hashed_password = User.hash_password(mot_de_passe)
        else:
            hashed_password = user.mot_de_passe

        user.update(nom, email, hashed_password, isadmin)
        flash('Utilisateur modifié avec succès!', 'success')
        return redirect(url_for('main.home'))

    return render_template('edit_user.html', user=user)

# Suppression utilisateur
@main.route('/delete_user/<int:id>', methods=['POST'])
@login_required
def delete_user(id):
    user = User.query.get_or_404(id)
    user.delete()
    flash('Utilisateur supprimé avec succès!', 'success')
    return redirect(url_for('main.home'))

# Login
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        mot_de_passe = request.form['mot_de_passe']
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(mot_de_passe):
            login_user(user)
            flash('Connexion réussie !', 'success')
            if user.isadmin:
                return redirect(url_for('main.home'))
            else:
                return redirect(url_for('main.dashboard'))
        else:
            flash('Identifiants incorrects.', 'danger')

    return render_template('login.html')

# Logout
@main.route('/logout')
def logout():
    logout_user()
    flash('Déconnexion réussie.', 'success')
    return redirect(url_for('main.login'))

# Ajout utilisateur protégé (admin only)
@main.route('/add_user_protected', methods=['POST'])
@login_required
def add_user_protected():
    if not current_user.isadmin:
        flash('Vous n\'avez pas les droits nécessaires.', 'danger')
        return redirect(url_for('main.home'))

    nom = request.form['nom']
    email = request.form['email']
    mot_de_passe = request.form['mot_de_passe']
    isadmin = True if request.form.get('isadmin') == 'on' else False
    hashed_password = User.hash_password(mot_de_passe)
    User.add(nom, email, hashed_password, isadmin)
    flash('Utilisateur ajouté avec succès!', 'success')
    return redirect(url_for('main.home'))

# Dashboard utilisateur non-admin
@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')
