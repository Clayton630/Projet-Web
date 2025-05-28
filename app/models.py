"""Modèles SQLAlchemy de l’application."""

# On importe des outils pour la sécurité des mots de passe
from werkzeug.security import generate_password_hash, check_password_hash
# UserMixin : permet à l’utilisateur d’être compatible avec Flask-Login (connexion, session, etc)
from flask_login import UserMixin

# On importe la base de données SQLAlchemy définie dans __init__.py
from . import db

# ------------- MODELE UTILISATEUR ----------------
class User(db.Model, UserMixin):
    """Utilisateur inscrit dans l’application."""

    __tablename__ = "utilisateurs"  # Nom de la table dans la base

    # Colonnes de la table :
    id_user = db.Column(db.Integer, primary_key=True)              # Identifiant unique (clé primaire)
    mot_de_passe = db.Column(db.String(128), nullable=False)       # Mot de passe hashé (jamais stocké en clair)
    nom = db.Column(db.String(50), nullable=False)                 # Nom de l’utilisateur
    email = db.Column(db.String(50), nullable=False, unique=True)  # Email (unique !)
    isadmin = db.Column(db.Boolean, nullable=False)                # Est-ce un admin ?

    def __repr__(self):
        # Affichage lisible d’un objet User (pour le debug/logs)
        return f"<User {self.nom}>"

    def get_id(self):
        # Pour Flask-Login : retourne l’identifiant de l’utilisateur (doit être une chaîne)
        return str(self.id_user)

    def check_password(self, mot_de_passe):
        """Vérifie le mot de passe fourni par l’utilisateur (compare au hash)."""
        return check_password_hash(self.mot_de_passe, mot_de_passe)

    @staticmethod
    def hash_password(mot_de_passe):
        """Crée le hash sécurisé d’un mot de passe."""
        return generate_password_hash(mot_de_passe)

    @staticmethod
    def get_by_id(id_):
        # Récupère un utilisateur par son id (pratique pour certains usages)
        return User.query.get(id_)

    @staticmethod
    def add(nom, email, mot_de_passe, isadmin):
        """Crée et ajoute un nouvel utilisateur à la base."""
        new_user = User(
            nom=nom,
            email=email,
            mot_de_passe=mot_de_passe,
            isadmin=isadmin,
        )
        db.session.add(new_user)
        db.session.commit()

    def update(self, nom, email, mot_de_passe, isadmin):
        """Met à jour les infos de l’utilisateur courant."""
        self.nom = nom
        self.email = email
        self.mot_de_passe = mot_de_passe
        self.isadmin = isadmin
        db.session.commit()

    def delete(self):
        """Supprime l’utilisateur de la base."""
        db.session.delete(self)
        db.session.commit()

# ------------- MODELE CATEGORIE ----------------
class Category(db.Model):
    """Catégorie d’établissements."""

    __tablename__ = "categories"

    id_cat = db.Column(db.Integer, primary_key=True)           # Identifiant unique de la catégorie
    nom = db.Column(db.String(50), nullable=False)             # Nom de la catégorie

    # Lien avec les établissements de cette catégorie (relation "un à plusieurs")
    etablissements = db.relationship("Etablissement", back_populates="categorie")

# ------------- MODELE ETABLISSEMENT ----------------
class Etablissement(db.Model):
    """Lieu référencé pouvant recevoir des retours."""

    __tablename__ = "etablissements"

    id_etab = db.Column(db.Integer, primary_key=True)             # Identifiant unique
    nom = db.Column(db.String(50), nullable=False)                # Nom de l’établissement
    adresse = db.Column(db.String(50), nullable=False)            # Adresse textuelle
    latitude = db.Column(db.Float)                                # Latitude GPS (optionnelle)
    longitude = db.Column(db.Float)                               # Longitude GPS (optionnelle)
    id_cat = db.Column(db.Integer, db.ForeignKey("categories.id_cat"))   # Lien vers la catégorie (clé étrangère)

    # Lien inverse vers la catégorie (accès direct à l’objet Category)
    categorie = db.relationship("Category", back_populates="etablissements")

    @staticmethod
    def add(nom, adresse, latitude, longitude, id_cat):
        """Crée et enregistre un nouvel établissement."""
        try:
            new_etab = Etablissement(
                nom=nom,
                adresse=adresse,
                latitude=latitude,
                longitude=longitude,
                id_cat=id_cat,
            )
            db.session.add(new_etab)
            db.session.commit()
            return new_etab
        except Exception:
            db.session.rollback()
            return None

# ------------- MODELE RETOUR (AVIS) ----------------
class Retour(db.Model):
    """Avis laissé par un utilisateur sur un établissement."""

    __tablename__ = "retours"

    id_retour = db.Column(db.String(50), primary_key=True)     # Identifiant de l’avis (peut être un UUID, string)
    note = db.Column(db.Integer, nullable=False)               # Note (ex: sur 5)
    commentaire = db.Column(db.String(150), nullable=False)    # Texte du commentaire
    date = db.Column(db.Date, nullable=False)                  # Date de l’avis

    id_user = db.Column(db.Integer, db.ForeignKey("utilisateurs.id_user"))         # Lien vers l’utilisateur
    id_etab = db.Column(db.Integer, db.ForeignKey("etablissements.id_etab"))       # Lien vers l’établissement
