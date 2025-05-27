"""Modèles SQLAlchemy de l’application."""

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from . import db


class User(db.Model, UserMixin):
    """Utilisateur inscrit dans l’application."""

    __tablename__ = "utilisateurs"

    id_user = db.Column(db.Integer, primary_key=True)
    mot_de_passe = db.Column(db.String(128), nullable=False)
    nom = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    isadmin = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"<User {self.nom}>"

    def get_id(self):
        return str(self.id_user)

    def check_password(self, mot_de_passe):
        """Vérifie le mot de passe fourni."""
        return check_password_hash(self.mot_de_passe, mot_de_passe)

    @staticmethod
    def hash_password(mot_de_passe):
        """Retourne le hash sécurisé d’un mot de passe."""
        return generate_password_hash(mot_de_passe)

    @staticmethod
    def get_by_id(id_):
        return User.query.get(id_)

    @staticmethod
    def add(nom, email, mot_de_passe, isadmin):
        """Crée et enregistre un nouvel utilisateur."""
        new_user = User(
            nom=nom,
            email=email,
            mot_de_passe=mot_de_passe,
            isadmin=isadmin,
        )
        db.session.add(new_user)
        db.session.commit()

    def update(self, nom, email, mot_de_passe, isadmin):
        """Met à jour les informations de l’utilisateur."""
        self.nom = nom
        self.email = email
        self.mot_de_passe = mot_de_passe
        self.isadmin = isadmin
        db.session.commit()

    def delete(self):
        """Supprime l’utilisateur."""
        db.session.delete(self)
        db.session.commit()


class Category(db.Model):
    """Catégorie d’établissements."""

    __tablename__ = "categories"

    id_cat = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)

    etablissements = db.relationship("Etablissement", back_populates="categorie")


class Etablissement(db.Model):
    """Lieu référencé pouvant recevoir des retours."""

    __tablename__ = "etablissements"

    id_etab = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    adresse = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    id_cat = db.Column(db.Integer, db.ForeignKey("categories.id_cat"))

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


class Retour(db.Model):
    """Avis laissé par un utilisateur sur un établissement."""

    __tablename__ = "retours"

    id_retour = db.Column(db.String(50), primary_key=True)
    note = db.Column(db.Integer, nullable=False)
    commentaire = db.Column(db.String(150), nullable=False)
    date = db.Column(db.Date, nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey("utilisateurs.id_user"))
    id_etab = db.Column(db.Integer, db.ForeignKey("etablissements.id_etab"))