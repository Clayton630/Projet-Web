from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db
from pprint import pprint

class User(db.Model, UserMixin):

    __tablename__ = 'utilisateurs'
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
        return check_password_hash(self.mot_de_passe, mot_de_passe)
    @staticmethod
    def hash_password(mot_de_passe):
        return generate_password_hash(mot_de_passe)
    @staticmethod
    def get_by_id(id):
        return User.query.get(id)
    @staticmethod
    def add(nom, email, mot_de_passe, isadmin):
        new_user = User(nom=nom, email=email, mot_de_passe=mot_de_passe, isadmin=isadmin)
        db.session.add(new_user)
        db.session.commit()
    def update(self, nom, email, mot_de_passe, isadmin):
        self.nom = nom
        self.email = email
        self.mot_de_passe = mot_de_passe
        self.isadmin = isadmin
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Category(db.Model):
    __tablename__ = 'categories'
    id_cat = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    etablissements = db.relationship('Etablissement', back_populates='categorie')

class Etablissement(db.Model):
    __tablename__ = 'etablissements'
    id_etab = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    adresse = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    id_cat = db.Column(db.Integer, db.ForeignKey('categories.id_cat'))
    categorie = db.relationship('Category', back_populates='etablissements')
    @staticmethod
    def add(nom, adresse, latitude, longitude, id_cat):
        try:
            new_etablissement = Etablissement(nom=nom, adresse=adresse, latitude=latitude, longitude=longitude, id_cat=id_cat)
        except Exception as e:
            print(f"Erreur lors de la création de l'établissement : {e}")
            return None
        try:
            db.session.add(new_etablissement)
            db.session.commit()
            return new_etablissement
        except Exception as e:
            print(f"Erreur lors de l'ajout de l'établissement à la session : {e}")
            return None

class Retour(db.Model):
    __tablename__ = 'retours'

    id_retour = db.Column(db.String(50), primary_key=True)
    note = db.Column(db.Integer, nullable=False)
    commentaire = db.Column(db.String(150), nullable=False)
    date = db.Column(db.Date, nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('utilisateurs.id_user'))
    id_etab = db.Column(db.Integer, db.ForeignKey('etablissements.id_etab'))