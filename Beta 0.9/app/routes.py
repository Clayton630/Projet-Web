from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from .models import Etablissement
from . import db
from pprint import pprint

main = Blueprint("main", __name__)


# Redirection de l'URL racine vers la page de login
@main.route("/")
def index():
    return redirect(url_for("main.login"))


# Page d'accueil pour les admins
@main.route("/dashboard")
@login_required
def dashboard():
    if not current_user.isadmin:
        flash("Accès réservé aux administrateurs.", "danger")
        return redirect(url_for("main.home"))
    users = User.query.all()
    return render_template("dashboard.html", users=users)


# Formulaire d'inscription
@main.route("/add_user", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        nom = request.form["nom"]
        email = request.form["email"]
        mot_de_passe = request.form["mot_de_passe"]
        isadmin = True if request.form.get("isadmin") == "on" else False
        user = User.query.filter_by(email=email).first()
        if user:
            flash("L'email est déjà utilisé.", "danger")
            return redirect(url_for("main.add_user"))
        hashed_password = User.hash_password(mot_de_passe)
        User.add(nom, email, hashed_password, isadmin)
        flash("Compte créé avec succès !", "success")
        return redirect(url_for("main.login"))

    return render_template("add_user.html")


# Modification utilisateur
@main.route("/edit_user/<int:id>", methods=["GET", "POST"])
@login_required
def edit_user(id):
    user = User.query.get_or_404(id)

    if request.method == "POST":
        nom = request.form["nom"]
        email = request.form["email"]
        mot_de_passe = request.form["mot_de_passe"]
        isadmin = True if request.form.get("isadmin") == "on" else False

        if mot_de_passe:
            hashed_password = User.hash_password(mot_de_passe)
        else:
            hashed_password = user.mot_de_passe

        user.update(nom, email, hashed_password, isadmin)
        flash("Utilisateur modifié avec succès!", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("edit_user.html", user=user)


# Suppression utilisateur
@main.route("/delete_user/<int:id>", methods=["POST"])
@login_required
def delete_user(id):
    user = User.query.get_or_404(id)
    user.delete()
    flash("Utilisateur supprimé avec succès!", "success")
    return redirect(url_for("main.dashboard"))


# Login
@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        mot_de_passe = request.form["mot_de_passe"]
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(mot_de_passe):
            login_user(user)
            flash("Connexion réussie !", "success")
            if user.isadmin:
                return redirect(url_for("main.dashboard"))
            else:
                return redirect(url_for("main.home"))
        else:
            flash("Identifiants incorrects.", "danger")

    return render_template("login.html")


# Logout
@main.route("/logout")
def logout():
    logout_user()
    flash("Déconnexion réussie.", "success")
    return redirect(url_for("main.login"))


# Ajout utilisateur protégé (admin only)
@main.route("/add_user_protected", methods=["POST"])
@login_required
def add_user_protected():
    if not current_user.isadmin:
        flash("Vous n'avez pas les droits nécessaires.", "danger")
        return redirect(url_for("main.dashboard"))

    nom = request.form["nom"]
    email = request.form["email"]
    mot_de_passe = request.form["mot_de_passe"]
    isadmin = True if request.form.get("isadmin") == "on" else False
    hashed_password = User.hash_password(mot_de_passe)
    User.add(nom, email, hashed_password, isadmin)
    flash("Utilisateur ajouté avec succès!", "success")
    return redirect(url_for("main.dashboard"))


# home utilisateur non-admin
@main.route("/home")
@login_required
def home():
    return render_template("home.html")


@main.route("/etablissements")
@login_required
def etablissements():
    if not current_user.isadmin:
        flash("Accès réservé aux administrateurs.", "danger")
        return redirect(url_for("main.home"))
    etablissements = db.session.query(db.Model.metadata.tables["etablissements"]).all()
    Category = db.Model.metadata.tables["categories"]
    letab = []
    for etablissement in etablissements:
        cat = (
            db.session.query(Category)
            .filter(Category.c.id_cat == etablissement.id_cat)
            .first()
        )
        nomCat = cat.nom if cat else None
        letab.append(
            {
                "id_etab": etablissement.id_etab,
                "nom": etablissement.nom,
                "adresse": etablissement.adresse,
                "latitude": etablissement.latitude,
                "longitude": etablissement.longitude,
                "id_cat": etablissement.id_cat,
                "nomCat": nomCat,
            }
        )
    return render_template("etablissements.html", etablissements=letab)


@main.route("/add_etablissement", methods=["GET", "POST"])
def add_etablissement():
    if request.method == "POST":
        nom = request.form["nom"]
        adresse = request.form["adresse"]
        latitude = request.form["latitude"]
        longitude = request.form["longitude"]
        id_cat = request.form["id_cat"]
        Etablissement.add(nom, adresse, latitude, longitude, id_cat)
        flash("Adresse ajoutée avec succès !", "success")
        return redirect(url_for("main.etablissements"))
    Category = db.Model.metadata.tables["categories"]
    categories = db.session.query(Category).all()
    return render_template("add_etablissement.html", categories=categories)


@main.route("/edit_etablissement/<int:id>", methods=["GET", "POST"])
@login_required
def edit_etablissement(id):
    etablissement = (
        db.session.query(db.Model.metadata.tables["etablissements"])
        .filter_by(id_etab=id)
        .first()
    )
    if request.method == "POST":
        nom = request.form["nom"]
        adresse = request.form["adresse"]
        latitude = request.form["latitude"]
        longitude = request.form["longitude"]
        id_cat = request.form["id_cat"]
        etablissement.nom = nom
        etablissement.adresse = adresse
        etablissement.latitude = latitude
        etablissement.longitude = longitude
        etablissement.id_cat = id_cat
        db.session.commit()
        flash("Adresse modifiée avec succès !", "success")
        return redirect(url_for("main.etablissements"))
    Category = db.Model.metadata.tables["categories"]
    categories = db.session.query(Category).all()
    return render_template(
        "edit_etablissement.html", etablissement=etablissement, categories=categories
    )


@main.route("/delete_etablissement/<int:id>", methods=["GET", "POST"])
@login_required
def delete_etablissement(id):
    pprint(id)
    try:
        etablissement = (
            db.session.query(db.Model.metadata.tables["etablissements"])
            .filter_by(id_etab=id)
            .first()
        )
        db.session.delete(etablissement)
        db.session.commit()
    except Exception as e:
        pprint(e)
    flash("Adresse supprimée avec succès !", "success")
    return redirect(url_for("main.etablissements"))


@main.route("/categories")
@login_required
def categories():
    if not current_user.isadmin:
        flash("Accès réservé aux administrateurs.", "danger")
        return redirect(url_for("main.home"))
    categories = db.session.query(db.Model.metadata.tables["categories"]).all()
    return render_template("categories.html", categories=categories)


@main.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        nom = request.form["nom"]
        new_category = db.Model.metadata.tables["categories"](nom=nom)
        db.session.add(new_category)
        db.session.commit()
        flash("Catégorie ajoutée avec succès !", "success")
        return redirect(url_for("main.categories"))
    return render_template("add_category.html")


@main.route("/edit_category/<int:id>", methods=["GET", "POST"])
@login_required
def edit_category(id):
    category = (
        db.session.query(db.Model.metadata.tables["categories"])
        .filter_by(id_cat=id)
        .first()
    )
    if request.method == "POST":
        nom = request.form["nom"]
        category.nom = nom
        db.session.commit()
        flash("Catégorie modifiée avec succès !", "success")
        return redirect(url_for("main.categories"))
    return render_template("edit_category.html", category=category)
