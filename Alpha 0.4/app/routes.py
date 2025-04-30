from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db
from werkzeug.security import check_password_hash

main = Blueprint('main', __name__)

# Route d'accueil
@main.route('/')
def home():
    users = User.query.all()
    return render_template('home.html', users=users)

# Route pour afficher le formulaire d'inscription et ajouter un utilisateur
@main.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        nom = request.form['nom']
        email = request.form['email']
        mot_de_passe = request.form['mot_de_passe']
        isadmin = True if request.form.get('isadmin') == 'on' else False

        # Vérifier si l'email existe déjà
        user = User.query.filter_by(email=email).first()
        if user:
            flash('L\'email est déjà utilisé.', 'danger')
            return redirect(url_for('main.add_user'))

        # Hash du mot de passe avant de l'ajouter à la base
        hashed_password = User.hash_password(mot_de_passe)
        User.add(nom, email, hashed_password, isadmin)
        flash('Compte créé avec succès !', 'success')
        return redirect(url_for('main.login'))

    return render_template('add_user.html')

# Route de modification d'un utilisateur
@main.route('/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    user = User.query.get_or_404(id)

    if request.method == 'POST':
        nom = request.form['nom']
        email = request.form['email']
        mot_de_passe = request.form['mot_de_passe']
        isadmin = True if request.form.get('isadmin') == 'on' else False

        user.update(nom, email, mot_de_passe, isadmin)
        flash('Utilisateur modifié avec succès!', 'success')
        return redirect(url_for('main.home'))

    return render_template('edit_user.html', user=user)

# Route pour supprimer un utilisateur
@main.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    user = User.query.get_or_404(id)
    user.delete()
    flash('Utilisateur supprimé avec succès!', 'success')
    return redirect(url_for('main.home'))

# Route pour afficher le formulaire de login
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        mot_de_passe = request.form['mot_de_passe']
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(mot_de_passe):
            login_user(user)
            flash('Connexion réussie !', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Identifiants incorrects.', 'danger')

    return render_template('login.html')

# Route pour déconnecter un utilisateur
@main.route('/logout')
def logout():
    logout_user()
    flash('Déconnexion réussie.', 'success')
    return redirect(url_for('main.home'))

# Route protégée pour ajouter un utilisateur (uniquement pour les admin ou utilisateurs connectés)
@main.route('/add_user_protected', methods=['POST'])
@login_required
def add_user_protected():
    if not current_user.isadmin:
        flash('Vous n\'avez pas les droits nécessaires pour effectuer cette action.', 'danger')
        return redirect(url_for('main.home'))

    nom = request.form['nom']
    email = request.form['email']
    mot_de_passe = request.form['mot_de_passe']
    isadmin = True if request.form.get('isadmin') == 'on' else False
    hashed_password = User.hash_password(mot_de_passe)
    User.add(nom, email, hashed_password, isadmin)
    flash('Utilisateur ajouté avec succès!', 'success')
    return redirect(url_for('main.home'))
