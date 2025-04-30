from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db

class User(db.Model, UserMixin):
    __tablename__ = 'Utilisateurs'
    
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
