"""Routes principales de l’application Flask, version sécurisée."""

from datetime import date
from functools import wraps

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)
from sqlalchemy import func

from . import db
from .models import Category, Etablissement, Retour, User

# --------------------------------------------------------------------------- #
# 1. DÉCORATEUR : ADMIN REQUIRED
# --------------------------------------------------------------------------- #

def admin_required(f):
    """
    Décorateur pour sécuriser l’accès à une route :
    - L’utilisateur doit être connecté ET admin.
    - Sinon, il est redirigé avec un message d’erreur.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not getattr(current_user, "isadmin", False):
            flash("Accès réservé aux administrateurs.", "danger")
            return redirect(url_for("main.home"))
        return f(*args, **kwargs)
    return decorated_function

# --------------------------------------------------------------------------- #
# 2. Blueprint principal
# --------------------------------------------------------------------------- #
main = Blueprint("main", __name__)

# --------------------------------------------------------------------------- #
# Authentification
# --------------------------------------------------------------------------- #

@main.route("/")
def index():
    """Redirige vers la page de connexion."""
    return redirect(url_for("main.login"))

@main.route("/login", methods=["GET", "POST"])
def login():
    """Affiche le formulaire puis authentifie l’utilisateur."""
    if request.method == "POST":
        email = request.form["email"]
        mot_de_passe = request.form["mot_de_passe"]
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(mot_de_passe):
            login_user(user)
            flash("Connexion réussie !", "success")
            return redirect(url_for("main.home"))
        flash("Identifiants incorrects.", "danger")
    return render_template("login.html")

@main.route("/logout")
def logout():
    """Termine la session courante."""
    logout_user()
    flash("Déconnexion réussie.", "success")
    return redirect(url_for("main.login"))

# --------------------------------------------------------------------------- #
# Tableau de bord administrateur
# --------------------------------------------------------------------------- #

@main.route("/dashboard")
@login_required
@admin_required
def dashboard():
    """Liste tous les utilisateurs (admin seulement)."""
    users = User.query.all()
    return render_template("dashboard.html", users=users)

# --------------------------------------------------------------------------- #
# Gestion des utilisateurs (admin uniquement)
# --------------------------------------------------------------------------- #

@main.route("/add_user", methods=["GET", "POST"])
def add_user():
    """
    Crée un compte public. (PAS admin !)
    Uniquement accessible aux non-connectés ou pour s’inscrire en tant que simple user.
    """
    if request.method == "POST":
        nom = request.form["nom"]
        email = request.form["email"]
        mot_de_passe = User.hash_password(request.form["mot_de_passe"])
        isadmin = request.form.get("isadmin") == "on"
        if User.query.filter_by(email=email).first():
            flash("L’e-mail est déjà utilisé.", "danger")
            return redirect(url_for("main.add_user"))
        User.add(nom, email, mot_de_passe, isadmin)
        flash("Compte créé avec succès !", "success")
        return redirect(url_for("main.login"))
    return render_template("add_user.html")

@main.route("/add_user_protected", methods=["POST"])
@login_required
@admin_required
def add_user_protected():
    """Ajoute un compte (admin uniquement)."""
    User.add(
        request.form["nom"],
        request.form["email"],
        User.hash_password(request.form["mot_de_passe"]),
        request.form.get("isadmin") == "on",
    )
    flash("Utilisateur ajouté.", "success")
    return redirect(url_for("main.dashboard"))

@main.route("/edit_user/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_user(id):
    """Modifie un utilisateur (admin uniquement)."""
    user = User.query.get_or_404(id)
    if request.method == "POST":
        mot_de_passe = (
            User.hash_password(request.form["mot_de_passe"])
            if request.form["mot_de_passe"]
            else user.mot_de_passe
        )
        user.update(
            request.form["nom"],
            request.form["email"],
            mot_de_passe,
            request.form.get("isadmin") == "on",
        )
        flash("Utilisateur modifié.", "success")
        return redirect(url_for("main.dashboard"))
    return render_template("edit_user.html", user=user)

@main.route("/delete_user/<int:id>", methods=["POST"])
@login_required
@admin_required
def delete_user(id):
    """Supprime un utilisateur (admin uniquement)."""
    User.query.get_or_404(id).delete()
    flash("Utilisateur supprimé.", "success")
    return redirect(url_for("main.dashboard"))

# --------------------------------------------------------------------------- #
# Accueil utilisateur (carte)
# --------------------------------------------------------------------------- #

@main.route("/home")
@login_required
def home():
    """Affiche la carte interactive et ses données."""
    etablissements_json = []
    for etab in Etablissement.query.all():
        moyenne = (
            db.session.query(func.avg(Retour.note))
            .filter_by(id_etab=etab.id_etab)
            .scalar()
        )
        etablissements_json.append(
            {
                "id_etab": etab.id_etab,
                "nom": etab.nom,
                "adresse": etab.adresse,
                "latitude": etab.latitude,
                "longitude": etab.longitude,
                "categorie": etab.categorie.nom if etab.categorie else "Non renseignée",
                "moyenne": round(float(moyenne), 2) if moyenne else None,
            }
        )
    categories = [cat.nom for cat in Category.query.all()]
    return render_template(
        "home.html",
        etablissements=etablissements_json,
        categories=categories,
    )

# --------------------------------------------------------------------------- #
# Gestion des établissements (admin uniquement)
# --------------------------------------------------------------------------- #

@main.route("/etablissements")
@login_required
@admin_required
def etablissements():
    """Liste les établissements (admin uniquement)."""
    return render_template(
        "etablissements.html", etablissements=Etablissement.query.all()
    )

@main.route("/add_etablissement", methods=["GET", "POST"])
@login_required
@admin_required
def add_etablissement():
    """Ajoute un nouvel établissement (admin uniquement)."""
    if request.method == "POST":
        Etablissement.add(
            request.form["nom"],
            request.form["adresse"],
            request.form["latitude"],
            request.form["longitude"],
            request.form["id_cat"],
        )
        flash("Adresse ajoutée.", "success")
        return redirect(url_for("main.etablissements"))
    return render_template("add_etablissement.html", categories=Category.query.all())

@main.route("/edit_etablissement/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_etablissement(id):
    """Modifie un établissement (admin uniquement)."""
    etablissement = Etablissement.query.get_or_404(id)
    if request.method == "POST":
        etablissement.nom = request.form["nom"]
        etablissement.adresse = request.form["adresse"]
        etablissement.latitude = request.form["latitude"]
        etablissement.longitude = request.form["longitude"]
        etablissement.id_cat = request.form["id_cat"]
        db.session.commit()
        flash("Établissement modifié.", "success")
        return redirect(url_for("main.etablissements"))
    return render_template(
        "edit_etablissement.html",
        etablissement=etablissement,
        categories=Category.query.all(),
    )

@main.route("/delete_etablissement/<int:id>", methods=["POST"])
@login_required
@admin_required
def delete_etablissement(id):
    """Supprime un établissement (admin uniquement)."""
    etab = Etablissement.query.get(id)
    if etab:
        db.session.delete(etab)
        db.session.commit()
        flash("Établissement supprimé.", "success")
    else:
        flash("Établissement non trouvé.", "danger")
    return redirect(url_for("main.etablissements"))

# --------------------------------------------------------------------------- #
# Gestion des catégories (admin uniquement)
# --------------------------------------------------------------------------- #

@main.route("/categories")
@login_required
@admin_required
def categories():
    """Liste les catégories (admin uniquement)."""
    return render_template("categories.html", categories=Category.query.all())

@main.route("/add_category", methods=["GET", "POST"])
@login_required
@admin_required
def add_category():
    """Ajoute une catégorie (admin uniquement)."""
    if request.method == "POST":
        db.session.add(Category(nom=request.form["nom"]))
        db.session.commit()
        flash("Catégorie ajoutée.", "success")
        return redirect(url_for("main.categories"))
    return render_template("add_category.html")

@main.route("/edit_category/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_category(id):
    """Modifie une catégorie existante (admin uniquement)."""
    category = Category.query.get_or_404(id)
    if request.method == "POST":
        category.nom = request.form["nom"]
        db.session.commit()
        flash("Catégorie modifiée.", "success")
        return redirect(url_for("main.categories"))
    return render_template("edit_category.html", category=category)

@main.route("/delete_category/<int:id>", methods=["POST"])
@login_required
@admin_required
def delete_category(id):
    """Supprime une catégorie (admin uniquement)."""
    category = Category.query.get(id)
    if category:
        db.session.delete(category)
        db.session.commit()
        flash("Catégorie supprimée.", "success")
    else:
        flash("Catégorie non trouvée.", "danger")
    return redirect(url_for("main.categories"))

# --------------------------------------------------------------------------- #
# Panneau latéral : fiche établissement (fragment AJAX)
# --------------------------------------------------------------------------- #

@main.route("/fiche_etablissement_fragment/<int:id>")
@login_required
def fiche_etablissement_fragment(id):
    """Retourne le fragment HTML fiche-établissement."""
    etab = Etablissement.query.get_or_404(id)
    avis = (
        db.session.query(Retour, User)
        .join(User, Retour.id_user == User.id_user)
        .filter(Retour.id_etab == id)
        .order_by(Retour.date.desc())
        .all()
    )
    notes = [a.note for a, _ in avis]
    moyenne = round(sum(notes) / len(notes), 2) if notes else None
    mon_avis = Retour.query.filter_by(
        id_user=current_user.id_user, id_etab=id
    ).first()
    return render_template(
        "fiche_etablissement_panel.html",
        etablissement=etab,
        avis=avis,
        moyenne=moyenne,
        mon_avis=mon_avis,
    )

# --------------------------------------------------------------------------- #
# Gestion des avis (public/user, admin seulement pour suppression commentaire)
# --------------------------------------------------------------------------- #

@main.route("/delete_commentaire/<id_retour>", methods=["POST"])
@login_required
def delete_commentaire(id_retour):
    """Supprime un commentaire (admin ou propriétaire du commentaire)."""
    avis = Retour.query.get_or_404(id_retour)
    if current_user.isadmin or avis.id_user == current_user.id_user:
        db.session.delete(avis)
        db.session.commit()
        flash("Commentaire supprimé.", "success")
    else:
        flash("Action non autorisée.", "danger")
    return redirect(url_for("main.home"))

@main.route("/etablissement/<int:id>", methods=["POST"])
@login_required
def gerer_avis(id):
    """Ajoute, modifie ou supprime un avis sur un établissement."""
    etab = Etablissement.query.get_or_404(id)
    action = request.form.get("action")

    if action == "add":
        if Retour.query.filter_by(id_user=current_user.id_user, id_etab=id).first():
            flash("Vous avez déjà déposé un avis.", "warning")
            return redirect(url_for("main.home"))
        db.session.add(
            Retour(
                id_retour=f"{current_user.id_user}-{id}-{date.today():%Y%m%d%H%M%S}",
                note=int(request.form["note"]),
                commentaire=request.form["commentaire"].strip(),
                date=date.today(),
                id_user=current_user.id_user,
                id_etab=id,
            )
        )
        db.session.commit()
        flash("Avis enregistré !", "success")

    elif action == "edit":
        mon_avis = Retour.query.filter_by(
            id_user=current_user.id_user, id_etab=id
        ).first()
        if not mon_avis:
            flash("Avis introuvable.", "danger")
        else:
            mon_avis.note = int(request.form["note"])
            mon_avis.commentaire = request.form["commentaire"].strip()
            mon_avis.date = date.today()
            db.session.commit()
            flash("Avis mis à jour.", "success")

    elif action == "delete":
        mon_avis = Retour.query.filter_by(
            id_user=current_user.id_user, id_etab=id
        ).first()
        if mon_avis:
            db.session.delete(mon_avis)
            db.session.commit()
            flash("Avis supprimé.", "success")
        else:
            flash("Avis introuvable.", "danger")

    else:
        flash("Action non reconnue.", "danger")

    return redirect(url_for("main.home"))
